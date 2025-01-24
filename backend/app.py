from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS
from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any
from config import DATABASE_CONFIG, GEMINI_API_KEY
from transformers import AutoTokenizer, AutoModelForCausalLM
import google.generativeai as genai


# Flask app
app = Flask(__name__)
CORS(app)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
# Database connection function
def get_db_connection():
    connection_string = (
        f"Driver={DATABASE_CONFIG['driver']};"
        f"Server={DATABASE_CONFIG['server']};"
        f"Database={DATABASE_CONFIG['database']};"
        f"Trusted_Connection={DATABASE_CONFIG['trusted_connection']}"
    )
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Define the graph state structure properly using TypedDict
class GraphState(TypedDict):
    user_input: str
    parsed_data: Dict[str, Any]
    sql_query: str
    result: List[Dict[str, Any]]

# Function to extract entities using LLaMA model (via Hugging Face)
def extract_entities(user_query: str) -> Dict[str, Any]:
    try:
        
        response = model.generate_content(
            f"""
            Consider I have only two tables in my store database: `products` and `suppliers` and the database is created with SQL Server (so process the queries according to it). 

            The schema of the `products` table is as follows:
            products (
                id INT PRIMARY KEY,
                name VARCHAR(255),
                brand VARCHAR(100),
                price DECIMAL(10,2),
                category VARCHAR(100),
                description TEXT,
                supplier_id INT REFERENCES suppliers(id)
            )

            The schema of the `suppliers` table is as follows:
            suppliers (
                id INT PRIMARY KEY,
                name VARCHAR(255),
                contactInfo VARCHAR(255),
                categoriesOffered TEXT
            )

            Find the entities from the following user query and convert it into an SQL query only. Do not provide any explanations in the response text. The response should not contain `\n`, `sql`, or ```.

            Example:
            If the user query is: "Which suppliers provide laptops?", the SQL query should be:
            Select * from suppliers where categoriesOffered like '%laptops%';
            Also if in any query you found the word 'suppliers' then it should refer to the `suppliers` table, do not remove the 's' from at the end. Similarly if in any query you found the word 'products' then it should refer to the `products` table, do not remove the 's' from at the end.

            User query:
            {user_query}
            """


        )
        sql_query = response.text.strip()
        sql_query = sql_query.strip("```sql\n")
        
        print("Generated SQL query:", sql_query)
        return {"sql_query": sql_query}

    except Exception as e:
        print(f"Error generating SQL query: {str(e)}")
        return {"sql_query": None}
        

# Node: Process user query
def process_user_query_node(state: GraphState) -> GraphState:
    user_query = state["user_input"].lower()

    extracted_data = extract_entities(user_query)
    sql_query = extracted_data.get("sql_query")
    if not sql_query:
        state["parsed_data"] = {"user_query" : user_query}
        state["sql_query"] = None
        return state
    
    state["parsed_data"] = {"user_query" : user_query}
    state["sql_query"] = sql_query
    return state

# Node: Generate SQL query
def generate_sql_query_node(state: GraphState) -> GraphState:
    sql_query = state["sql_query"]
    if not sql_query:
        state['sql_query'] = None
        state['result'] = [{"error": "No valid SQL query generated"}]
    else:
        state['sql_query'] = sql_query
    return state

# Node: Execute SQL query
def execute_sql_query_node(state: GraphState) -> GraphState:
    sql_query = state["sql_query"]
    if not sql_query:
        state["result"] = [{"error": "Invalid or unrecognized query"}]
        return state

    try:
        conn = get_db_connection()
        if not conn:
            state["result"] = [{"error": "Failed to connect to database"}]
            return state
        
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()

        if not results:
            state["result"] = [{"error": "No results found"}]
            return state

        columns = [column[0] for column in cursor.description]
        state["result"] = [dict(zip(columns, row)) for row in results]
    except Exception as e:
        state["result"] = [{"error": f"Error executing query: {str(e)}"}]
    return state

# Initialize the StateGraph with proper typing
workflow = StateGraph(GraphState)

# Add nodes to the graph
workflow.add_node("process_user_query", process_user_query_node)
workflow.add_node("generate_sql_query", generate_sql_query_node)
workflow.add_node("execute_sql_query", execute_sql_query_node)

# Connect the nodes properly
workflow.add_edge("process_user_query", "generate_sql_query")
workflow.add_edge("generate_sql_query", "execute_sql_query")

# Set entry point for the graph
workflow.set_entry_point("process_user_query")

# Compile the workflow
app_chain = workflow.compile()

# Flask route to handle user input
@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_query = request.json.get("query")
        if not user_query:
            return jsonify({"error": "Query not provided"}), 400

        # Create initial state with proper typing
        initial_state: GraphState = {
            "user_input": user_query,
            "parsed_data": {},
            "sql_query": "",
            "result": []
        }

        # Execute the workflow with the initial state
        result = app_chain.invoke(initial_state)
        
        # Print query information
        print("\n=== Query Information ===")
        print(f"User Query: {user_query}")
        print(f"Parsed Data: {result['parsed_data']}")
        print(f"SQL Query: {result['sql_query']}")
        print("=====================\n")

        # Summarize the result using the generative model
        query_result = result["result"]
        if query_result and isinstance(query_result, list) and "error" not in query_result[0]:
            prompt = f"""
    You are an assistant that summarizes SQL query results for a user.
    Here's the user's query: "{user_query}"
    SQL query executed: "{result['sql_query']}"
    Query results: {query_result}

    Provide a natural language summary of these results in proper markdown format also strictly following these guidelines:
    - Use `#` for main headings (like the title of the section).
    - Use `##` for subheadings (for sub-sections).
    - Use `**bold**` for important terms or emphasis.
    - Use `*italic*` for less emphasized terms.
    - Use `-` or `*` for bullet points to list items.
    - Use `1.` for numbered lists if applicable.
    - To create a line break or new line (<br>), end a line with two or more spaces, and then type return.
    - Avoid using `\n` for line breaks; let markdown format the content properly.
    - Do not use any inline styles, unnecessary characters, or HTML tags like <h1>, <p>, <ul>, or <li>.

    The markdown should be well-structured, readable, and easy to understand, using the appropriate formatting for each section of the summary.
"""




            try:
                response = model.generate_content(prompt)
                summary = response.text.strip()
            except Exception as e:
                summary = "Error generating summary: " + str(e)
        else:
            summary = "No results found or query error."

        # Return both the query information and the generated summary
        return jsonify({
            "debug_info": {
                "user_query": user_query,
                "parsed_data": result['parsed_data'],
                "sql_query": result['sql_query']
            },
            "response": {
                "raw_results": query_result,
                "summary": summary
            }
        })
    except Exception as e:
        return jsonify({"error": f"Error processing query: {str(e)}"}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)

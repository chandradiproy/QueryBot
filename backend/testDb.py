import google.generativeai as genai

genai.configure(api_key="AIzaSyDU7tplHDPVPxuprBoap8GfiwxjdtnC8OU")
model = genai.GenerativeModel("gemini-1.5-flash")
user_prompt = "Show all the sellers who sells laptops"
response = model.generate_content(f"find the entites from {user_prompt} and convert it into a sql query only, Do not give other explanations. ")
print(response.text)
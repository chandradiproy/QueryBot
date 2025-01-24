import React, { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Markdown from "react-markdown";
import Navbar from "./components/Navbar";
import ChatContainer from "./components/ChatContainer";
import InputBar from "./components/InputBar";

function App() {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Add the user's message to the chat
    setMessages([...messages, { text: userInput, sender: "user" }]);

    // Send the user's message to the backend
    try {
      const response = await axios.post("http://127.0.0.1:5000/ask", {
        query: userInput,
      });
      const botMessage =
        response.data.response || "Sorry, I couldn't process your request.";

      // Add the bot's response to the chat
      setMessages([
        ...messages,
        { text: userInput, sender: "user" },
        { text: botMessage, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error sending query:", error);
      setMessages([
        ...messages,
        { text: "An error occurred. Please try again.", sender: "bot" },
      ]);
    }

    // Clear the input field
    setUserInput("");
  };

  return (
    <main className="flex flex-col sm:h-screen h-svh w-full dark:bg-zinc-800 bg-gray-100 items-center ">
      <Navbar/>
      <section className="flex overflow-y-auto justify-center w-full  h-full ">
        <ChatContainer/>
      </section>
       <InputBar/>
    </main>
  );
}

export default App;

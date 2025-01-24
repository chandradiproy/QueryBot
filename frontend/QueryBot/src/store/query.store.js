import { create } from "zustand";
import { axiosInstance } from "../lib/axios";

export const useQueryStore = create((set) => ({
  isLoading: false,
  messages: [],

  getInfo: async (user_input) => {
    // Add user input to messages first
    set((state) => ({
      isLoading: true,
      messages: [...state.messages, { text: user_input, sender: "user" }],
    }));

    try {
      const response = await axiosInstance.post("/ask", {
        query: user_input,
      });

    //   console.log("Response Data:", response.data); // Debugging log

      // Extract the summary from the response
      const botMessage =
        response.data?.response?.summary || "Sorry, no summary available.";

      // Add the bot's response (summary) to the messages
     
      set((state) => ({
        messages: [
          ...state.messages,
          { text: botMessage, sender: "bot" },
        ],
      }));
    } catch (error) {
      console.error("Error sending query", error);
      // Add error message if something went wrong
      set((state) => ({
        messages: [
          ...state.messages,
          { text: "An error occurred. Please try again.", sender: "bot" },
        ],
      }));
    } finally {
      set({ isLoading: false }); // Set loading to false after request completion
    }
  },
}));

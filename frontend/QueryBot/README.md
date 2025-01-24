
# QueryBot - Chat Application

## Overview

QueryBot is a chat application designed to simulate a conversation between a user and a bot. It allows the user to ask queries, and the bot responds with detailed answers, powered by a backend API. The app provides an interactive, real-time chat experience, with real-time responses and markdown support for text formatting.

## Features

- **User Interaction**: The user can input queries, and the bot will respond in real-time.
- **Bot Responses**: The bot's responses are dynamically generated and displayed with Markdown formatting support.
- **Message Styling**: Messages from the user are displayed on the right, while messages from the bot appear on the left.
- **Loading State**: The bot shows a loading animation when processing the user's query.
- **Scrolling**: The chat container auto-scrolls to the latest message, ensuring the user always sees the most recent messages.

## Tech Stack

- **Frontend**: React.js, Tailwind CSS, Lucide Icons, React Markdown
- **Backend**: Flask or Node.js (assuming backend is implemented and running on `http://127.0.0.1:5000/ask` for this demo)
- **State Management**: Zustand for managing global state
- **Markdown Rendering**: React Markdown with GFM (GitHub Flavored Markdown) plugin for Markdown rendering
- **Icons**: Lucide Icons for bot and user representation

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/querybot.git
cd querybot
```

### 2. Install Dependencies

```bash
npm install
```

This will install all the necessary dependencies for the project.

### 3. Set up the Backend

For the demo to work, the app expects a backend API at `http://127.0.0.1:5000/ask`. If you don't have the backend ready yet, you can simulate the responses by modifying the `axios` call in `App.js` or use any mock API.

### 4. Run the App

Once everything is set up, you can run the app in development mode.

```bash
npm start
```

Your application will be available at `http://localhost:3000` in the browser.

## Structure

Here's a breakdown of the file structure:

```
/querybot
│
├── /src
│   ├── /components
│   │   ├── ChatContainer.jsx      # Chat UI and message display
│   │   ├── InputBar.jsx          # User input and message submission
│   │   ├── Navbar.jsx            # Application header/navbar
│   ├── /store
│   │   ├── query.store.js        # Zustand store for managing state (messages, loading state)
│   ├── App.jsx                    # Main component that ties everything together
│   ├── index.js                  # React entry point
├── /public
│   ├── index.html                # HTML template
├── /node_modules                 # Dependencies
├── package.json                  # Project configuration and dependencies
├── tailwind.config.js            # Tailwind CSS configuration
└── README.md                     # Project Documentation
```

### Components

- **`ChatContainer.js`**: Displays the conversation, handling both user and bot messages. Messages are styled and rendered dynamically based on their sender.
- **`InputBar.js`**: Manages the user input, triggering the query submission to the backend and updating the message state.
- **`Navbar.js`**: Simple navigation bar for the app's UI.

### Store

- **`query.store.js`**: Zustand store for managing the global state of messages and loading states. This store tracks the chat messages and whether the bot is loading a response.

## Functionality

### 1. **Message Flow**

When the user types a query and submits it:
- The query is sent to the backend API (`/ask`).
- The user's message is added to the message state and displayed on the right.
- While waiting for the response, a loading spinner appears.
- Once the response is received, the bot's message is added to the message state and displayed on the left.

### 2. **Styling**

Messages are styled using **Tailwind CSS** to distinguish between the user's messages and the bot's messages:
- **User Messages**: Displayed on the right with a blue background (`bg-blue-500`) and white text.
- **Bot Messages**: Displayed on the left with a gray background (`bg-gray-200`) and black text.
- **Icons**: The bot’s icon (`Bot`) appears alongside the bot’s message, while the user’s icon (`User2`) appears with the user’s message.
- **Loading State**: The bot's message container shows an ellipsis animation when the bot is "typing."

### 3. **Auto-Scrolling**

To improve user experience, the chat window auto-scrolls to the bottom to show the most recent messages using `ScrollToBottom`.

### 4. **Markdown Rendering**

Both user and bot messages support Markdown rendering, allowing for text formatting (bold, italic, links, etc.) using the `ReactMarkdown` component with the `remark-gfm` plugin for GitHub-flavored markdown.

## Notes

- **Keyboard Behavior**: The app ensures that the messages container adapts to the height of the on-screen keyboard when using mobile devices. This may require additional customization depending on the environment.
  
- **Error Handling**: In case of an error during the API request, a generic error message will be displayed instead of the bot’s response.

## Future Improvements

- **Backend Integration**: The backend is currently a mock API. Integrate with a real backend that processes queries and provides intelligent responses.
- **User Authentication**: Add user authentication for personalized experiences.
- **Enhanced UI**: Add features such as avatars for the bot, emojis, or richer text formatting.
- **Message History**: Store chat history in local storage or a database to retrieve and display previous conversations.

## Contributing

Feel free to open issues and pull requests! If you want to contribute, follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

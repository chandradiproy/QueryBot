import React, { useEffect, useRef } from 'react';
import InputBar from './InputBar';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useQueryStore } from '../store/query.store';
import { Bot, Ellipsis, User2 } from 'lucide-react';

function ChatContainer() {
  const { messages, isLoading } = useQueryStore();
  const endOfMessagesRef = useRef(null); // Ref to the end of the messages container

  // Scroll to the bottom whenever messages change
  useEffect(() => {
    if (endOfMessagesRef.current) {
      endOfMessagesRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]); // Trigger the effect when messages change

  return (
    <div className='md:w-3xl w-full pt-2 px-4 h-full relative flex flex-col justify-between overflow-y-auto'>
      <div className="space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500">No messages yet</div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-md p-3 rounded-lg  ${message.sender === 'user' ? 'dark:bg-zinc-700 bg-gray-200 dark:text-white' : ' dark:text-gray-200 text-black'}`}
              >
                {message.sender === 'bot' ? (
                  <Bot size={30} className="dark:text-white text-black " />
                ) : (
                  <User2 size={30} className="dark:text-white text-black" />
                )}
                {isLoading && message.sender === 'bot' && (
                  <Ellipsis size={30} className="dark:text-white text-black animate-ping" />
                )}
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.text}
                </ReactMarkdown>
              </div>
            </div>
          ))
        )}
      </div>

      {/* This div will ensure we scroll to it */}
      <div ref={endOfMessagesRef} className="h-1" />
    </div>
  );
}

export default ChatContainer;

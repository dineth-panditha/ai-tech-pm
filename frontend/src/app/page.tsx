"use client";

import { useChat } from "../hooks/useChat";
import ChatHeader from "../components/ChatHeader";
import ChatMessage from "../components/ChatMessage";
import ChatInput from "../components/ChatInput";

export default function Home() {
  const { messages, isLoading, sendMessage } = useChat();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-3xl bg-white rounded-xl shadow-lg overflow-hidden flex flex-col h-[80vh]">
        
        <ChatHeader />

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="text-gray-400 text-center mt-20">
              Start chatting with your AI Project Manager! <br/>
              Try asking: "Do we have any open bugs in GitHub?"
            </div>
          ) : (
            messages.map((msg, index) => (
              <ChatMessage key={index} message={msg} />
            ))
          )}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-800 p-3 rounded-lg rounded-bl-none animate-pulse">
                AI is thinking...
              </div>
            </div>
          )}
        </div>

        <ChatInput onSendMessage={sendMessage} isLoading={isLoading} />

      </div>
    </div>
  );
}
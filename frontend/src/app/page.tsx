"use client";

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<{ role: string; content: string }[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    // User ගේ මැසේජ් එක UI එකට දානවා
    const newChat = [...chatHistory, { role: "user", content: message }];
    setChatHistory(newChat);
    setMessage("");
    setIsLoading(true);

    try {
      // අපේ Python Backend එකට කතා කරනවා
      const res = await fetch("http://127.0.0.1:8000/api/v1/chat/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message }),
      });
      
      const data = await res.json();
      
      // AI ගේ උත්තරේ UI එකට දානවා (data.response හෝ කෙලින්ම data එන විදිය අනුව)
      const aiResponse = typeof data === 'string' ? data : data.response || "No response";
      
      setChatHistory([...newChat, { role: "ai", content: aiResponse }]);
    } catch (error) {
      setChatHistory([...newChat, { role: "ai", content: "❌ Error: Could not connect to the backend server." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-3xl bg-white rounded-xl shadow-lg overflow-hidden flex flex-col h-[80vh]">
        
        {/* Header */}
        <div className="bg-blue-600 text-white p-4 font-bold text-xl text-center">
          🤖 AI Tech Project Manager
        </div>

        {/* Chat History Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {chatHistory.length === 0 ? (
            <div className="text-gray-400 text-center mt-20">
              Start chatting with your AI Project Manager! <br/>
              Try asking: "Do we have any open bugs in GitHub?"
            </div>
          ) : (
            chatHistory.map((chat, index) => (
              <div key={index} className={`flex ${chat.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[80%] p-3 rounded-lg ${
                  chat.role === "user" ? "bg-blue-500 text-white rounded-br-none" : "bg-gray-200 text-gray-800 rounded-bl-none"
                }`}>
                  {chat.content}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-800 p-3 rounded-lg rounded-bl-none animate-pulse">
                AI is thinking...
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 bg-gray-100 flex gap-2 border-t">
          <input
            type="text"
            className="flex-1 p-3 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500 text-gray-800"
            placeholder="Ask about your project..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors disabled:bg-blue-400"
          >
            Send
          </button>
        </div>

      </div>
    </div>
  );
}
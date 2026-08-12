import { useState } from "react";
import { Message } from "../types/chat";

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    const newMessages: Message[] = [...messages, { role: "user", content }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const res = await fetch(`${API_URL}/api/v1/chat/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: content }),
      });
      
      const data = await res.json();
      const aiResponse = typeof data === 'string' ? data : data.response || "No response";
      
      setMessages([...newMessages, { role: "ai", content: aiResponse }]);
    } catch (error) {
      setMessages([...newMessages, { role: "ai", content: "❌ Error: Could not connect to the backend server." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return { messages, isLoading, sendMessage };
};
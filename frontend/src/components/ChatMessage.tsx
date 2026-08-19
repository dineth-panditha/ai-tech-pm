import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Message } from "../types/chat";

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} animate-in fade-in slide-in-from-bottom-2 duration-300`}>
      <div className={`max-w-[85%] p-4 rounded-2xl ${
        isUser 
          ? "bg-blue-600 text-white rounded-br-sm shadow-sm" 
          : "bg-white border border-gray-200 text-gray-800 rounded-bl-sm shadow-sm"
      }`}>
        {isUser ? (
          <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
        ) : (
          <div className="prose prose-sm md:prose-base max-w-none prose-blue">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
export default function ChatHeader() {
  return (
    <div className="bg-blue-600 px-6 py-4 flex items-center space-x-4 shadow-sm z-10">
      <div className="relative">
        <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center text-xl">
          🤖
        </div>
        <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-400 border-2 border-blue-600 rounded-full"></div>
      </div>
      <div>
        <h1 className="text-white font-bold text-lg tracking-wide">Tech Lead Agent</h1>
        <p className="text-blue-100 text-xs font-medium tracking-wider uppercase">Online & Ready</p>
      </div>
    </div>
  );
}
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ModernAIChatUI() {

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! Ask me anything."
    }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {

    if (!input.trim()) return;

    const userMessage = {
      role: "user",
      content: input
    };

    setMessages(prev => [...prev, userMessage]);

    setLoading(true);

    try {

      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "qwen2.5-coder:7b",
          stream: false,
          messages: [
            {
              role: "user",
              content: input
            }
          ]
        })
      });

      const data = await response.json();

      const assistantMessage = {
        role: "assistant",
        content: data.response
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: "Error connecting to backend."
        }
      ]);

    } finally {

      setLoading(false);
      setInput("");

    }
  };

  return (
    <div className="h-screen flex bg-zinc-950 text-white">

      {/* Sidebar */}
      <aside className="w-72 border-r border-zinc-800 bg-zinc-900 p-4 flex flex-col">

        <button className="bg-white text-black rounded-xl py-3 font-medium mb-4">
          + New Chat
        </button>

        <div className="space-y-2">
          <div className="bg-zinc-800 p-3 rounded-xl text-sm">
            AI Chat Session
          </div>
        </div>

      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col">

        {/* Header */}
        <header className="border-b border-zinc-800 px-6 py-4 flex justify-between">

          <div>
            <h1 className="text-lg font-semibold">
              AI Assistant
            </h1>

            <p className="text-sm text-zinc-400">
              Ollama + Qwen2.5-7B
            </p>
          </div>

          <div className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm h-fit">
            Online
          </div>

        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">

          {messages.map((message, index) => (

            <div
              key={index}
              className={`flex ${
                message.role === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >

              <div
                className={`max-w-3xl px-5 py-4 rounded-2xl ${
                  message.role === "user"
                    ? "bg-white text-black"
                    : "bg-zinc-800 text-zinc-100"
                }`}
              >

                <div className="text-xs uppercase mb-2 opacity-60">
                  {message.role}
                </div>

                <div className="prose prose-invert max-w-none">

                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </ReactMarkdown>

                </div>

              </div>

            </div>

          ))}

          {loading && (
            <div className="flex justify-start">

              <div className="bg-zinc-800 rounded-2xl px-5 py-4 flex gap-2">

                <div className="w-2 h-2 bg-white rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-150" />
                <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-300" />

              </div>

            </div>
          )}

        </div>

        {/* Input */}
        <div className="border-t border-zinc-800 p-5">

          <div className="flex gap-4">

            <textarea
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything..."
              className="flex-1 resize-none rounded-2xl bg-zinc-900 border border-zinc-700 px-5 py-4 text-white outline-none"
            />

            <button
              onClick={sendMessage}
              disabled={loading}
              className="bg-white text-black rounded-2xl px-6 py-4 font-medium"
            >
              Send
            </button>

          </div>

        </div>

      </main>

    </div>
  );
}
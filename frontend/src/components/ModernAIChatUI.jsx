import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function ModernAIChatUI() {

  // =========================================
  // CURRENT CHAT MESSAGES
  // =========================================
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Welcome to ai-platform.\n\nYour local AI workspace is ready."
    }
  ]);

  // =========================================
  // CONVERSATIONS
  // =========================================
  const [conversations, setConversations] = useState([]);

  // =========================================
  // ACTIVE CONVERSATION
  // =========================================
  const [activeConversationId, setActiveConversationId] = useState(null);

  // =========================================
  // INPUT + LOADING
  // =========================================
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // =========================================
  // LOAD CONVERSATIONS ON STARTUP
  // =========================================
  useEffect(() => {
    fetchConversations();
  }, []);

  // =========================================
  // FETCH CONVERSATIONS
  // =========================================
  const fetchConversations = async () => {

    try {

      const response = await fetch(
        "http://localhost:8000/conversations/"
      );

      const data = await response.json();

      // Show only latest 5
      setConversations(data.slice(0, 5));

    } catch (error) {

      console.error(
        "Failed to fetch conversations",
        error
      );

    }
  };

  // =========================================
  // LOAD CONVERSATION
  // =========================================
  const loadConversation = async (conversationId) => {

    try {

      const response = await fetch(
        `http://localhost:8000/conversations/${conversationId}`
      );

      const data = await response.json();

      setMessages(data);

      setActiveConversationId(conversationId);

    } catch (error) {

      console.error(
        "Failed to load conversation",
        error
      );

    }
  };

  // =========================================
  // START NEW CHAT
  // =========================================
  const startNewChat = () => {

    setActiveConversationId(null);

    setMessages([
      {
        role: "assistant",
        content:
          "New chat started.\n\nHow can I help you today?"
      }
    ]);

  };

  // =========================================
  // SEND MESSAGE
  // =========================================
  const sendMessage = async () => {

    if (!input.trim() || loading) return;

    const currentInput = input;

    // Clear immediately
    setInput("");

    const userMessage = {
      role: "user",
      content: currentInput
    };

    // Instant UI update
    setMessages(prev => [
      ...prev,
      userMessage
    ]);

    setLoading(true);

    try {

      const response = await fetch(
        "http://localhost:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            conversation_id: activeConversationId,
            model: "qwen2.5-coder:7b",
            stream: false,

            messages: [
              {
                role: "user",
                content: currentInput
              }
            ]
          })
        }
      );

      const data = await response.json();

      // Save conversation ID
      if (!activeConversationId && data.conversation_id) {

        setActiveConversationId(
          data.conversation_id
        );

        fetchConversations();
      }

      const assistantMessage = {
        role: "assistant",
        content: data.response
      };

      setMessages(prev => [
        ...prev,
        assistantMessage
      ]);

    } catch (error) {

      console.error(error);

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content:
            "Failed to connect to backend."
        }
      ]);

    } finally {

      setLoading(false);

    }
  };

  // =========================================
  // ENTER TO SEND
  // SHIFT+ENTER FOR NEWLINE
  // =========================================
  const handleKeyDown = (e) => {

    if (e.key === "Enter" && !e.shiftKey) {

      e.preventDefault();

      sendMessage();
    }
  };

  return (

    <div className="h-screen bg-black text-white flex overflow-hidden">

      {/* ========================================= */}
      {/* SIDEBAR */}
      {/* ========================================= */}
      <aside className="w-80 bg-zinc-950 border-r border-zinc-800 flex flex-col">

        {/* Logo */}
        <div className="px-6 py-6 border-b border-zinc-800">

          <div className="flex items-center gap-3">

            <div className="
              w-10
              h-10
              rounded-2xl
              bg-white
              text-black
              flex
              items-center
              justify-center
              font-bold
              text-lg
            ">
              AI
            </div>

            <div>

              <h1 className="font-semibold text-lg">
                ai-platform
              </h1>

              <p className="text-xs text-zinc-500">
                Local AI Workspace
              </p>

            </div>

          </div>

        </div>

        {/* New Chat */}
        <div className="p-4">

          <button
            onClick={startNewChat}
            className="
              w-full
              rounded-2xl
              bg-white
              text-black
              py-4
              font-semibold
              transition-all
              hover:scale-[1.02]
              active:scale-[0.98]
            "
          >
            + New Chat
          </button>

        </div>

        {/* Conversations */}
        <div className="flex-1 overflow-y-auto px-4 pb-4">

          <div className="
            text-xs
            uppercase
            tracking-wider
            text-zinc-500
            px-2
            mb-3
          ">
            Recent Conversations
          </div>

          <div className="space-y-2">

            {conversations.length === 0 && (

              <div className="text-sm text-zinc-600 px-2">
                No conversations yet
              </div>

            )}

            {conversations.map((conversation) => (

              <button
                key={conversation.id}
                onClick={() =>
                  loadConversation(conversation.id)
                }
                className={`
                  w-full
                  text-left
                  rounded-2xl
                  p-4
                  transition-all
                  border
                  ${
                    activeConversationId === conversation.id
                      ? "bg-zinc-800 border-zinc-700"
                      : "bg-zinc-900 border-zinc-900 hover:bg-zinc-800 hover:border-zinc-800"
                  }
                `}
              >

                <div className="
                  font-medium
                  text-sm
                  truncate
                ">
                  {conversation.title || "Untitled Chat"}
                </div>

                <div className="
                  text-xs
                  text-zinc-500
                  mt-1
                ">
                  Persistent session
                </div>

              </button>

            ))}

          </div>

        </div>

      </aside>

      {/* ========================================= */}
      {/* MAIN */}
      {/* ========================================= */}
      <main className="
        flex-1
        flex
        flex-col
        bg-gradient-to-b
        from-zinc-950
        to-black
      ">

        {/* Header */}
        <header className="
          border-b
          border-zinc-800
          px-8
          py-5
          backdrop-blur-xl
          bg-black/40
        ">

          <div className="
            flex
            items-center
            justify-between
          ">

            <div>

              <h2 className="text-xl font-semibold">
                AI Assistant
              </h2>

              <p className="text-sm text-zinc-500 mt-1">
                Powered by Ollama + Qwen2.5-Coder 7B
              </p>

            </div>

            <div className="
              px-4
              py-2
              rounded-full
              bg-emerald-500/10
              border
              border-emerald-500/20
              text-emerald-400
              text-sm
            ">
              ● Online
            </div>

          </div>

        </header>

        {/* ========================================= */}
        {/* MESSAGES */}
        {/* ========================================= */}
        <div className="
          flex-1
          overflow-y-auto
          px-8
          py-8
          space-y-8
        ">

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
                className={`
                  max-w-4xl
                  rounded-3xl
                  px-6
                  py-5
                  shadow-2xl
                  border
                  backdrop-blur-xl
                  ${
                    message.role === "user"
                      ? `
                        bg-white
                        text-black
                        border-white
                      `
                      : `
                        bg-zinc-900/80
                        text-zinc-100
                        border-zinc-800
                      `
                  }
                `}
              >

                <div className="
                  text-xs
                  uppercase
                  tracking-widest
                  opacity-50
                  mb-4
                ">
                  {message.role}
                </div>

                <div className="
                  prose
                  prose-invert
                  max-w-none
                ">

                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                  >
                    {message.content}
                  </ReactMarkdown>

                </div>

              </div>

            </div>

          ))}

          {/* Loading */}
          {loading && (

            <div className="flex justify-start">

              <div className="
                bg-zinc-900
                border
                border-zinc-800
                rounded-3xl
                px-6
                py-5
                flex
                gap-2
              ">

                <div className="w-2 h-2 bg-white rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-150" />
                <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-300" />

              </div>

            </div>

          )}

        </div>

        {/* ========================================= */}
        {/* INPUT */}
        {/* ========================================= */}
        <div className="
          border-t
          border-zinc-800
          bg-black/50
          backdrop-blur-xl
          p-6
        ">

          <div className="
            max-w-5xl
            mx-auto
            flex
            gap-4
            items-end
          ">

            <textarea
              rows={1}
              value={input}
              onChange={(e) =>
                setInput(e.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Message ai-platform..."
              className="
                flex-1
                resize-none
                rounded-3xl
                bg-zinc-900
                border
                border-zinc-800
                px-6
                py-5
                text-white
                outline-none
                focus:border-zinc-600
                transition
              "
            />

            <button
              onClick={sendMessage}
              disabled={loading}
              className="
                rounded-3xl
                bg-white
                text-black
                px-8
                py-5
                font-semibold
                transition-all
                hover:scale-[1.03]
                active:scale-[0.98]
                disabled:opacity-50
              "
            >
              Send
            </button>

          </div>

        </div>

      </main>

    </div>

  );
}
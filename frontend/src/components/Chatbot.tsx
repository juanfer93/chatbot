import { FC, useRef, useEffect } from "react";
import { useStore } from "../store/useStore";

const Chatbot: FC = () => {
  const {
    messages,
    userInput,
    isVisible,
    isLoading,
    setUserInput,
    toggleVisibility,
    addMessage,
    resetMessages,
    setLoading,
  } = useStore();

  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const messageEndRef = useRef<HTMLDivElement | null>(null);

  
  const handleSendMessage = async () => {
    if (!userInput.trim()) return;
    
    const userMessage = {
      id: Date.now().toString(),
      text: userInput,
      sender: "user" as const,
    };
    addMessage(userMessage);

    setUserInput("");
    setLoading(true);

    try {
      const response = await fetch(`${backendUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
      });

      const data = await response.json();
      const botMessage = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        sender: "bot" as const,
      };
      addMessage(botMessage);
    } catch (error) {
      console.error("Error al conectar con el backend:", error);
      addMessage({
        id: (Date.now() + 2).toString(),
        text: "Hubo un error al conectar con el servidor.",
        sender: "bot" as const,
      });
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    if (messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);
  
  return (
    <div>
      <button
        onClick={toggleVisibility}
        className="fixed bottom-4 right-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-full shadow-lg hover:scale-110 transition-transform"
      >
        {isVisible ? "Cerrar Chat" : "Abrir Chat"}
      </button>

      {isVisible && (
        <div
          className={`fixed bottom-16 right-4 w-96 h-[450px] bg-white border border-gray-200 rounded-lg shadow-xl flex flex-col ${
            isVisible ? "animate-fade-in" : "animate-fade-out"
          }`}
        >
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 flex justify-between items-center rounded-t-lg">
            <h2 className="text-lg font-bold">Chatbot</h2>
            <button
              onClick={resetMessages}
              className="bg-red-500 px-2 py-1 text-sm rounded hover:bg-red-600 transition-colors"
            >
              Reset
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-2">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`p-3 rounded-lg ${
                  msg.sender === "user"
                    ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white"
                    : "bg-gray-200 text-gray-800"
                }`}
              >
                <p className="text-center">{msg.text}</p>
              </div>
            ))}
            {isLoading && (
              <div className="bg-gray-200 p-3 rounded-lg animate-pulse text-center">
                Escribiendo...
              </div>
            )}
            <div ref={messageEndRef}></div>
          </div>

          <div className="p-4 border-t border-gray-200 flex items-center">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  handleSendMessage();
                }
              }}
              className="flex-1 border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Escribe un mensaje..."
            />
            <button
              onClick={handleSendMessage}
              className="ml-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg hover:scale-110 transition-transform"
            >
              Enviar
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
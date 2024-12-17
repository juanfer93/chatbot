import React from "react";
import { useStore } from "../store/useStore";

const Chatbot: React.FC = () => {
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

  return (
    <div>
      <button
        onClick={toggleVisibility}
        className="fixed bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg"
      >
        {isVisible ? "Cerrar Chat" : "Abrir Chat"}
      </button>

      {isVisible && (
        <div className="fixed bottom-16 right-4 w-80 h-96 bg-gray-100 border rounded-lg shadow-lg flex flex-col">
          <div className="bg-blue-500 text-white p-4 flex justify-between items-center">
            <h2 className="text-lg font-bold">Chatbot</h2>
            <button
              onClick={resetMessages}
              className="bg-red-500 px-2 py-1 text-sm rounded"
            >
              Reset
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-2">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`p-2 rounded-lg ${
                  msg.sender === "user"
                    ? "bg-blue-100 self-end"
                    : "bg-gray-300 self-start"
                }`}
              >
                {msg.text}
              </div>
            ))}
            {isLoading && <div className="text-gray-500">Escribiendo...</div>}
          </div>

          <div className="p-4 border-t flex items-center">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              className="flex-1 border rounded-lg p-2 focus:outline-none focus:ring focus:ring-blue-300"
              placeholder="Escribe un mensaje..."
            />
            <button
              onClick={handleSendMessage}
              className="ml-2 bg-blue-500 text-white px-4 py-2 rounded-lg"
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

import { create } from "zustand";

type Sender = "user" | "bot";

interface Message {
  id: string; 
  text: string;
  sender: Sender;
}

interface ChatbotStore {
  messages: Message[];
  userInput: string;
  isVisible: boolean;
  isLoading: boolean;

  setUserInput: (input: string) => void;
  toggleVisibility: () => void;
  addMessage: (message: Message) => void;
  resetMessages: () => void;
  setLoading: (loading: boolean) => void;
}

export const useStore = create<ChatbotStore>((set) => ({
  messages: [],
  userInput: "",
  isVisible: false,
  isLoading: false,

  setUserInput: (input: string) =>
    set(() => ({
      userInput: input,
    })),
  toggleVisibility: () =>
    set((state) => ({
      isVisible: !state.isVisible,
    })),
  addMessage: (message: Message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),
  resetMessages: () =>
    set(() => ({
      messages: [],
    })),
  setLoading: (loading: boolean) =>
    set(() => ({
      isLoading: loading,
    })),
}));

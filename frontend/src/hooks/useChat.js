import { useState, useCallback, useEffect } from "react";
import { sendMessage, checkHealth, getSystemInfo } from "@/services/api";

/**
 * Custom hook to manage chat state and interactions
 */
export const useChat = () => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isConnected, setIsConnected] = useState(false);
    const [systemInfo, setSystemInfo] = useState(null);
    const [error, setError] = useState(null);

    // Check backend health on mount
    useEffect(() => {
        const checkConnection = async () => {
            try {
                const health = await checkHealth();
                setIsConnected(health.status === "healthy");

                const info = await getSystemInfo();
                setSystemInfo(info);
            } catch (err) {
                console.error("Failed to connect to backend:", err);
                setIsConnected(false);
                setError(
                    "Unable to connect to the backend. Please ensure the server is running."
                );
            }
        };

        checkConnection();
    }, []);

    /**
     * Send a user message and get bot response
     */
    const sendUserMessage = useCallback(async (userMessage) => {
        if (!userMessage.trim()) return;

        // Add user message to chat
        const userMsg = {
            id: Date.now(),
            type: "user",
            content: userMessage,
            timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, userMsg]);
        setIsLoading(true);
        setError(null);

        try {
            // Get bot response
            const response = await sendMessage(userMessage);

            // Add bot message to chat
            const botMsg = {
                id: Date.now() + 1,
                type: "bot",
                content: response.answer,
                sources: response.sources,
                timestamp: response.timestamp,
            };

            setMessages((prev) => [...prev, botMsg]);
        } catch (err) {
            console.error("Failed to send message:", err);

            // Add error message
            const errorMsg = {
                id: Date.now() + 1,
                type: "error",
                content:
                    err.message ||
                    "Failed to get response from the chatbot. Please try again.",
                timestamp: new Date().toISOString(),
            };

            setMessages((prev) => [...prev, errorMsg]);
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    }, []);

    /**
     * Clear all messages
     */
    const clearMessages = useCallback(() => {
        setMessages([]);
        setError(null);
    }, []);

    /**
     * Retry last message if there was an error
     */
    const retryLastMessage = useCallback(() => {
        const lastUserMessage = [...messages]
            .reverse()
            .find((msg) => msg.type === "user");

        if (lastUserMessage) {
            // Remove error messages after the last user message
            const userMsgIndex = messages.findIndex(
                (msg) => msg.id === lastUserMessage.id
            );
            setMessages((prev) => prev.slice(0, userMsgIndex + 1));
            sendUserMessage(lastUserMessage.content);
        }
    }, [messages, sendUserMessage]);

    return {
        messages,
        isLoading,
        isConnected,
        systemInfo,
        error,
        sendUserMessage,
        clearMessages,
        retryLastMessage,
    };
};

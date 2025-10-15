import "./App.css";
import { useChat } from "@/hooks/useChat";
import Header from "@/components/Header";
import ChatContainer from "@/components/ChatContainer";
import ChatInput from "@/components/ChatInput";
import { Card } from "@/components/ui/card";
import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

function App() {
    const {
        messages,
        isLoading,
        isConnected,
        systemInfo,
        error,
        sendUserMessage,
        clearMessages,
        retryLastMessage,
    } = useChat();

    return (
        <div className="h-screen flex flex-col bg-background">
            {/* Header */}
            <Header
                isConnected={isConnected}
                onClearChat={clearMessages}
                messageCount={messages.length}
                systemInfo={systemInfo}
            />

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Connection Error Banner */}
                {!isConnected && (
                    <div className="bg-red-50 dark:bg-red-950 border-b border-red-200 dark:border-red-800 px-4 py-3">
                        <div className="container mx-auto flex items-center gap-2 text-sm text-red-700 dark:text-red-300">
                            <AlertCircle className="h-4 w-4 flex-shrink-0" />
                            <span>
                                Unable to connect to the backend. Please ensure
                                the FastAPI server is running on{" "}
                                <code className="bg-red-100 dark:bg-red-900 px-1 py-0.5 rounded">
                                    http://localhost:8000
                                </code>
                            </span>
                        </div>
                    </div>
                )}

                {/* Chat Messages */}
                <ChatContainer messages={messages} isLoading={isLoading} />

                {/* Input Area */}
                <div className="border-t bg-card/50 backdrop-blur">
                    <div className="container mx-auto px-4 py-4">
                        <ChatInput
                            onSendMessage={sendUserMessage}
                            isLoading={isLoading}
                            disabled={!isConnected}
                        />

                        {/* Error Message */}
                        {error && (
                            <div className="mt-2 flex items-center justify-between gap-2 text-sm text-red-600 dark:text-red-400">
                                <div className="flex items-center gap-2">
                                    <AlertCircle className="h-4 w-4" />
                                    <span>{error}</span>
                                </div>
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={retryLastMessage}
                                    className="text-red-600 hover:text-red-700 dark:text-red-400"
                                >
                                    Retry
                                </Button>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;

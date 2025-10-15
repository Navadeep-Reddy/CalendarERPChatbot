import { useEffect, useRef } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import ChatMessage from "./ChatMessage";
import { MessageSquare, Sparkles } from "lucide-react";

/**
 * ChatContainer Component
 * Displays message history with auto-scroll and empty state
 */
const ChatContainer = ({ messages, isLoading }) => {
    const scrollRef = useRef(null);
    const bottomRef = useRef(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        if (bottomRef.current) {
            bottomRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages, isLoading]);

    // Empty state
    if (messages.length === 0 && !isLoading) {
        return (
            <div className="flex-1 flex items-center justify-center p-8">
                <Card className="max-w-md p-8 text-center border-dashed">
                    <div className="flex justify-center mb-4">
                        <div className="rounded-full bg-emerald-100 dark:bg-emerald-900 p-4">
                            <MessageSquare className="h-8 w-8 text-emerald-600 dark:text-emerald-400" />
                        </div>
                    </div>
                    <h3 className="text-xl font-semibold mb-2">
                        Welcome to ERP Calendar Assistant
                    </h3>
                    <p className="text-muted-foreground mb-4">
                        Ask me anything about calendar events, schedules, or
                        activities.
                    </p>
                    <div className="space-y-2 text-sm text-left">
                        <div className="flex items-start gap-2">
                            <Sparkles className="h-4 w-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                            <span className="text-muted-foreground">
                                "What events are happening this week?"
                            </span>
                        </div>
                        <div className="flex items-start gap-2">
                            <Sparkles className="h-4 w-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                            <span className="text-muted-foreground">
                                "Tell me about upcoming workshops"
                            </span>
                        </div>
                        <div className="flex items-start gap-2">
                            <Sparkles className="h-4 w-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                            <span className="text-muted-foreground">
                                "What activities are available for students?"
                            </span>
                        </div>
                    </div>
                </Card>
            </div>
        );
    }

    return (
        <ScrollArea className="flex-1 px-4" ref={scrollRef}>
            <div className="max-w-4xl mx-auto py-4">
                {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                ))}

                {/* Loading indicator */}
                {isLoading && (
                    <div className="flex gap-3 mb-4 animate-in fade-in slide-in-from-bottom-2 duration-300">
                        <div className="h-8 w-8 mt-1 rounded-full bg-emerald-500 flex items-center justify-center">
                            <div className="h-4 w-4 text-white">
                                <svg
                                    className="animate-spin"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                >
                                    <circle
                                        className="opacity-25"
                                        cx="12"
                                        cy="12"
                                        r="10"
                                        stroke="currentColor"
                                        strokeWidth="4"
                                    />
                                    <path
                                        className="opacity-75"
                                        fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                    />
                                </svg>
                            </div>
                        </div>
                        <div className="flex-1 space-y-2">
                            <div className="flex items-center gap-2">
                                <span className="text-sm font-semibold">
                                    ERP Assistant
                                </span>
                            </div>
                            <Card className="p-4 max-w-[85%] bg-card border-border">
                                <div className="flex gap-1">
                                    <div
                                        className="h-2 w-2 bg-emerald-500 rounded-full animate-bounce"
                                        style={{ animationDelay: "0ms" }}
                                    />
                                    <div
                                        className="h-2 w-2 bg-emerald-500 rounded-full animate-bounce"
                                        style={{ animationDelay: "150ms" }}
                                    />
                                    <div
                                        className="h-2 w-2 bg-emerald-500 rounded-full animate-bounce"
                                        style={{ animationDelay: "300ms" }}
                                    />
                                </div>
                            </Card>
                        </div>
                    </div>
                )}

                {/* Scroll anchor */}
                <div ref={bottomRef} />
            </div>
        </ScrollArea>
    );
};

export default ChatContainer;

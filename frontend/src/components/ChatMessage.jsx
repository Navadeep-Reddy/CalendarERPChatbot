import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Bot, User, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import SourceDocument from "./SourceDocument";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * ChatMessage Component
 * Displays individual chat messages with different styles for user/bot/error
 */
const ChatMessage = ({ message }) => {
    const isUser = message.type === "user";
    const isError = message.type === "error";
    const isBot = message.type === "bot";

    const formatTime = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
        });
    };

    return (
        <div
            className={cn(
                "flex gap-3 mb-4 animate-in fade-in slide-in-from-bottom-2 duration-300",
                isUser && "flex-row-reverse"
            )}
        >
            {/* Avatar */}
            <Avatar
                className={cn(
                    "h-8 w-8 mt-1",
                    isUser && "bg-blue-500",
                    isBot && "bg-emerald-500",
                    isError && "bg-red-500"
                )}
            >
                <AvatarFallback className="bg-transparent">
                    {isUser && <User className="h-4 w-4 text-white" />}
                    {isBot && <Bot className="h-4 w-4 text-white" />}
                    {isError && <AlertCircle className="h-4 w-4 text-white" />}
                </AvatarFallback>
            </Avatar>

            {/* Message Content */}
            <div
                className={cn(
                    "flex-1 space-y-2",
                    isUser && "flex flex-col items-end"
                )}
            >
                {/* Message Header */}
                <div
                    className={cn(
                        "flex items-center gap-2",
                        isUser && "flex-row-reverse"
                    )}
                >
                    <span className="text-sm font-semibold">
                        {isUser && "You"}
                        {isBot && "ERP Assistant"}
                        {isError && "System"}
                    </span>
                    <span className="text-xs text-muted-foreground">
                        {formatTime(message.timestamp)}
                    </span>
                </div>

                {/* Message Bubble */}
                <Card
                    className={cn(
                        "p-4 max-w-[85%]",
                        isUser && "bg-blue-500 text-white border-blue-600",
                        isBot && "bg-card border-border",
                        isError &&
                            "bg-red-50 border-red-200 dark:bg-red-950 dark:border-red-800"
                    )}
                >
                    {isBot ? (
                        <div
                            className={cn(
                                "text-sm prose prose-sm dark:prose-invert max-w-none",
                                "prose-p:my-1 prose-ul:my-1 prose-li:my-0",
                                "prose-headings:mt-2 prose-headings:mb-1"
                            )}
                        >
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                {message.content}
                            </ReactMarkdown>
                        </div>
                    ) : (
                        <p
                            className={cn(
                                "text-sm whitespace-pre-wrap break-words",
                                isError && "text-red-700 dark:text-red-300"
                            )}
                        >
                            {message.content}
                        </p>
                    )}
                </Card>

                {/* Source Documents */}
                {isBot && message.sources && message.sources.length > 0 && (
                    <div className="space-y-2 max-w-[85%]">
                        <div className="flex items-center gap-2">
                            <Badge variant="secondary" className="text-xs">
                                Sources ({message.sources.length})
                            </Badge>
                        </div>
                        <div className="space-y-2">
                            {message.sources.map((source, index) => (
                                <SourceDocument
                                    key={index}
                                    source={source}
                                    index={index}
                                />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ChatMessage;

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Send, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

/**
 * ChatInput Component
 * Handles user input with send button and loading states
 */
const ChatInput = ({ onSendMessage, isLoading, disabled }) => {
    const [inputValue, setInputValue] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!inputValue.trim() || isLoading || disabled) return;

        onSendMessage(inputValue);
        setInputValue("");
    };

    const handleKeyDown = (e) => {
        // Send on Enter, new line on Shift+Enter
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex gap-2 items-end">
            <div className="flex-1">
                <Input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder={
                        disabled
                            ? "Connect to backend to start chatting..."
                            : "Ask about calendar events, schedules, or activities..."
                    }
                    disabled={isLoading || disabled}
                    className={cn(
                        "resize-none min-h-[44px] max-h-[120px]",
                        "focus-visible:ring-2 focus-visible:ring-emerald-500"
                    )}
                />
            </div>
            <Button
                type="submit"
                size="default"
                disabled={!inputValue.trim() || isLoading || disabled}
                className={cn(
                    "h-[44px] px-4",
                    "bg-emerald-500 hover:bg-emerald-600 text-white",
                    "disabled:opacity-50"
                )}
            >
                {isLoading ? (
                    <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span className="ml-2 hidden sm:inline">
                            Sending...
                        </span>
                    </>
                ) : (
                    <>
                        <Send className="h-4 w-4" />
                        <span className="ml-2 hidden sm:inline">Send</span>
                    </>
                )}
            </Button>
        </form>
    );
};

export default ChatInput;

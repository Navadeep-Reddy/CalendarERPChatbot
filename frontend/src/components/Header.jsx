import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Calendar, Trash2, RefreshCw } from "lucide-react";
import { cn } from "@/lib/utils";

/**
 * Header Component
 * Displays app branding, connection status, and controls
 */
const Header = ({ isConnected, onClearChat, messageCount, systemInfo }) => {
    return (
        <header className="border-b bg-card/50 backdrop-blur supports-[backdrop-filter]:bg-card/50">
            <div className="container mx-auto px-4 py-3">
                <div className="flex items-center justify-between">
                    {/* Branding */}
                    <div className="flex items-center gap-3">
                        <div className="rounded-lg bg-emerald-500 p-2">
                            <Calendar className="h-5 w-5 text-white" />
                        </div>
                        <div>
                            <h1 className="text-lg font-bold">
                                ERP Calendar Assistant
                            </h1>
                            <p className="text-xs text-muted-foreground">
                                Powered by Gemini 2.5 Flash & RAG
                            </p>
                        </div>
                    </div>

                    {/* Status & Controls */}
                    <div className="flex items-center gap-3">
                        {/* System Info */}
                        {systemInfo && (
                            <div className="hidden md:flex items-center gap-2 text-xs text-muted-foreground">
                                <span>
                                    Model:{" "}
                                    {systemInfo.llm_model
                                        ?.split("-")
                                        .slice(0, 2)
                                        .join("-") || "N/A"}
                                </span>
                                <span>•</span>
                                <span>
                                    Docs:{" "}
                                    {systemInfo.vector_db_status
                                        ?.document_count || 0}
                                </span>
                            </div>
                        )}

                        {/* Connection Status */}
                        <Badge
                            variant={isConnected ? "default" : "destructive"}
                            className={cn(
                                "gap-1.5",
                                isConnected &&
                                    "bg-emerald-500 hover:bg-emerald-600"
                            )}
                        >
                            <div
                                className={cn(
                                    "h-2 w-2 rounded-full",
                                    isConnected
                                        ? "bg-white animate-pulse"
                                        : "bg-white"
                                )}
                            />
                            <span className="text-xs">
                                {isConnected ? "Connected" : "Disconnected"}
                            </span>
                        </Badge>

                        {/* Clear Chat Button */}
                        {messageCount > 0 && (
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={onClearChat}
                                className="gap-2 text-muted-foreground hover:text-foreground"
                            >
                                <Trash2 className="h-4 w-4" />
                                <span className="hidden sm:inline">Clear</span>
                            </Button>
                        )}
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;

import { Card, CardContent } from "@/components/ui/card";
import { FileText, Calendar } from "lucide-react";
import { cn } from "@/lib/utils";

/**
 * SourceDocument Component
 * Displays source document references from RAG retrieval
 */
const SourceDocument = ({ source, index }) => {
    // Parse source content - backend returns objects with page_content and metadata
    const content = source.page_content || source.content || "";
    const metadata = source.metadata || {};

    // Truncate content for display
    const truncateContent = (text, maxLength = 150) => {
        if (!text) return "No content available";
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + "...";
    };

    return (
        <Card className="bg-muted/50 border-muted hover:border-muted-foreground/20 transition-colors">
            <CardContent className="p-3">
                <div className="flex gap-3">
                    {/* Icon */}
                    <div className="mt-1">
                        {metadata.source?.includes("pdf") ||
                        metadata.source?.includes("PDF") ? (
                            <FileText className="h-4 w-4 text-muted-foreground" />
                        ) : (
                            <Calendar className="h-4 w-4 text-muted-foreground" />
                        )}
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                            <span className="text-xs font-medium text-muted-foreground">
                                Source {index + 1}
                            </span>
                            {metadata.page && (
                                <span className="text-xs text-muted-foreground">
                                    • Page {metadata.page}
                                </span>
                            )}
                            {metadata.source && (
                                <span className="text-xs text-muted-foreground truncate">
                                    • {metadata.source.split("/").pop()}
                                </span>
                            )}
                        </div>
                        <p className="text-xs text-muted-foreground leading-relaxed">
                            {truncateContent(content)}
                        </p>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};

export default SourceDocument;

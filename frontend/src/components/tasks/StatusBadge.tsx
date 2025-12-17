import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface StatusBadgeProps {
  completed: boolean;
}

export default function StatusBadge({ completed }: StatusBadgeProps) {
  return (
    <Badge
      className={cn(
        "font-medium",
        // T143: Enhanced contrast for WCAG 2.1 AA compliance
        completed
          ? "bg-green-100 text-green-900 border-green-300 hover:bg-green-200"
          : "bg-blue-100 text-blue-900 border-blue-300 hover:bg-blue-200"
      )}
      variant="outline"
    >
      {completed ? "Completed" : "Pending"}
    </Badge>
  );
}

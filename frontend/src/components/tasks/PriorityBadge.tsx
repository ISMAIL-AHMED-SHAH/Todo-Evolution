import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export type Priority = 'High' | 'Medium' | 'Low';

interface PriorityBadgeProps {
  priority: Priority;
}

/**
 * PriorityBadge - Color-coded badge component for task priority levels
 *
 * Displays priority with color coding:
 * - High: Red badge (bg-red-200)
 * - Medium: Orange badge (bg-orange-200)
 * - Low: Green badge (bg-green-200)
 *
 * @param priority - Task priority level ('High' | 'Medium' | 'Low')
 */
export default function PriorityBadge({ priority }: PriorityBadgeProps) {
  // T143: Map priority to color classes with WCAG 2.1 AA compliant contrast ratios
  const colorClasses = {
    High: "bg-red-200 text-red-900 hover:bg-red-200 font-medium",
    Medium: "bg-orange-200 text-orange-900 hover:bg-orange-200 font-medium",
    Low: "bg-green-200 text-green-900 hover:bg-green-200 font-medium",
  };

  return (
    <Badge
      className={cn(
        "border-transparent",
        colorClasses[priority]
      )}
    >
      {priority}
    </Badge>
  );
}

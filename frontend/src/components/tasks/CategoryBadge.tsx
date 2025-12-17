import * as React from "react";
import { Badge } from "@/components/ui/badge";

interface CategoryBadgeProps {
  categories: string[];
}

/**
 * CategoryBadge Component
 *
 * Displays task categories as a collection of small badges.
 *
 * @param categories - Array of category tag strings
 *
 * Validation rules (from data-model.md):
 * - Each category tag: max 50 characters
 * - Maximum 10 categories per task
 * - Categories are case-sensitive
 * - Empty array is valid (renders nothing)
 */
export default function CategoryBadge({ categories }: CategoryBadgeProps) {
  // Handle empty array - don't render anything
  if (!categories || categories.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-wrap gap-1.5">
      {categories.map((category, index) => (
        <Badge
          key={`${category}-${index}`}
          variant="secondary"
          className="bg-slate-100 text-slate-700 hover:bg-slate-200 border-slate-200"
        >
          {category}
        </Badge>
      ))}
    </div>
  );
}

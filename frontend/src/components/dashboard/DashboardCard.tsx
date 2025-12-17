/**
 * DashboardCard Component - Phase 2 UI/UX
 *
 * Interactive card with:
 * - Color-coded background
 * - Icon/emoji
 * - Title
 * - Count badge (optional)
 * - Framer Motion hover animations
 */

'use client';

import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface DashboardCardProps {
  title: string;
  emoji: string;
  backgroundColor: string;
  count?: number;
  badge?: string;
  onClick?: () => void;
}

export default function DashboardCard({
  title,
  emoji,
  backgroundColor,
  count,
  badge,
  onClick,
}: DashboardCardProps) {
  return (
    <motion.div
      // T145: Performance optimized hover animation
      whileHover={{
        scale: 1.05,
        willChange: 'transform',
        transition: { duration: 0.15, ease: [0.4, 0, 0.2, 1] },
      }}
      whileTap={{ scale: 0.98 }}
      style={{ willChange: 'auto' }}
    >
      <Card
        className={`cursor-pointer ${backgroundColor} border-none shadow-lg hover:shadow-xl transition-shadow`}
        onClick={onClick}
        role="button"
        tabIndex={0}
        aria-label={`${title}${badge ? `: ${badge}` : count !== undefined ? `: ${count} ${count === 1 ? 'task' : 'tasks'}` : ''}`}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onClick?.();
          }
        }}
      >
        <CardContent className="p-4 sm:p-5 md:p-6 flex flex-col items-center justify-center text-center space-y-3 sm:space-y-3.5 md:space-y-4 min-h-[140px] sm:min-h-[160px] md:min-h-[180px]">
          {/* Emoji Icon */}
          <div className="text-4xl sm:text-[2.75rem] md:text-5xl">
            {emoji}
          </div>

          {/* Title */}
          <h3 className="text-base sm:text-[1.0625rem] md:text-lg font-semibold text-gray-800 break-words w-full px-1">
            {title}
          </h3>

          {/* Count or Custom Badge (if provided) - T143: Enhanced contrast for WCAG 2.1 AA */}
          {badge && (
            <Badge variant="secondary" className="bg-white/90 text-gray-900 text-xs sm:text-[0.8125rem] md:text-sm px-2 sm:px-2.5 md:px-3 py-1 break-words max-w-full font-medium">
              {badge}
            </Badge>
          )}
          {!badge && count !== undefined && (
            <Badge variant="secondary" className="bg-white/90 text-gray-900 text-xs sm:text-[0.8125rem] md:text-sm px-2 sm:px-2.5 md:px-3 py-1 font-medium">
              {count} {count === 1 ? 'task' : 'tasks'}
            </Badge>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

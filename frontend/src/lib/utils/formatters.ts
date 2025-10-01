/**
 * Formatting utility functions
 */

import { format, formatDistanceToNow, parseISO, differenceInDays } from 'date-fns';

/**
 * Format date string to readable format
 */
export const formatDate = (dateString: string | undefined, formatStr = 'PPP'): string => {
  if (!dateString) return 'N/A';
  try {
    return format(parseISO(dateString), formatStr);
  } catch {
    return 'Invalid date';
  }
};

/**
 * Format date to relative time (e.g., "2 days ago")
 */
export const formatRelativeTime = (dateString: string | undefined): string => {
  if (!dateString) return 'Never';
  try {
    return formatDistanceToNow(parseISO(dateString), { addSuffix: true });
  } catch {
    return 'Invalid date';
  }
};

/**
 * Format time in minutes to hours and minutes
 */
export const formatTime = (minutes: number | undefined): string => {
  if (!minutes) return 'N/A';
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
};

/**
 * Calculate total time from prep and cook time
 */
export const calculateTotalTime = (
  prepTime: number | undefined,
  cookTime: number | undefined
): number => {
  return (prepTime || 0) + (cookTime || 0);
};

/**
 * Format quantity with unit
 */
export const formatQuantity = (quantity: number | undefined, unit: string | undefined): string => {
  if (!quantity) return unit || '';
  if (!unit) return quantity.toString();
  return `${quantity} ${unit}`;
};

/**
 * Calculate days until expiration
 */
export const daysUntilExpiration = (expirationDate: string | undefined): number | null => {
  if (!expirationDate) return null;
  try {
    return differenceInDays(parseISO(expirationDate), new Date());
  } catch {
    return null;
  }
};

/**
 * Format rating percentage
 */
export const formatRatingPercentage = (thumbsUp: number, total: number): string => {
  if (total === 0) return '0%';
  return `${Math.round((thumbsUp / total) * 100)}%`;
};

/**
 * Pluralize word based on count
 */
export const pluralize = (count: number, singular: string, plural?: string): string => {
  if (count === 1) return singular;
  return plural || `${singular}s`;
};

/**
 * Truncate text with ellipsis
 */
export const truncate = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Format user role
 */
export const formatRole = (role: string): string => {
  return role.charAt(0).toUpperCase() + role.slice(1);
};

/**
 * Get initials from username
 */
export const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
};

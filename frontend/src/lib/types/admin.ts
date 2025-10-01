/**
 * Admin-related types
 */

export interface AppSettings {
  favorites_threshold: number; // 0-1 (percentage)
  favorites_min_raters: number;
  rotation_period_days: number;
  low_stock_threshold_percent: number; // 0-1
  expiration_warning_days: number;
  updated_at: string;
}

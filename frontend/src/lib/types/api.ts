/**
 * Common API types and interfaces
 */

export interface ApiError {
  error: string;
  message: string;
  details?: Record<string, unknown>;
}

export interface Pagination {
  page: number;
  limit: number;
  total_pages: number;
  total_items: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: Pagination;
}

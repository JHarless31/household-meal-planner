/**
 * User-related types
 */

export type UserRole = 'admin' | 'user' | 'child';

export interface User {
  id: string;
  username: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  last_login?: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  role: UserRole;
}

export interface UserUpdate {
  username?: string;
  email?: string;
  password?: string;
  role?: UserRole;
  is_active?: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  message: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

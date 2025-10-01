/**
 * Validation utility functions
 */

/**
 * Validate email format
 */
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Validate URL format
 */
export const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

/**
 * Validate password strength
 * At least 8 characters
 */
export const isValidPassword = (password: string): boolean => {
  return password.length >= 8;
};

/**
 * Get password strength
 */
export const getPasswordStrength = (password: string): 'weak' | 'medium' | 'strong' => {
  if (password.length < 8) return 'weak';

  let strength = 0;
  if (password.length >= 12) strength++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
  if (/\d/.test(password)) strength++;
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;

  if (strength >= 3) return 'strong';
  if (strength >= 1) return 'medium';
  return 'weak';
};

/**
 * Validate date is Monday (for menu plans)
 */
export const isMonday = (date: Date): boolean => {
  return date.getDay() === 1;
};

/**
 * Validate required field
 */
export const isRequired = (value: unknown): boolean => {
  if (typeof value === 'string') return value.trim().length > 0;
  if (typeof value === 'number') return !isNaN(value);
  if (Array.isArray(value)) return value.length > 0;
  return value !== null && value !== undefined;
};

/**
 * Validate number range
 */
export const isInRange = (value: number, min: number, max: number): boolean => {
  return value >= min && value <= max;
};

/**
 * Validate positive number
 */
export const isPositive = (value: number): boolean => {
  return value > 0;
};

/**
 * Sanitize HTML to prevent XSS
 */
export const sanitizeHtml = (html: string): string => {
  const div = document.createElement('div');
  div.textContent = html;
  return div.innerHTML;
};

import { apiClient } from '@/services/apiClient';

// لایه‌ی ارتباط با بک‌اند مخصوص این فیچر.
// کامپوننت‌ها و هوک‌ها هرگز مستقیم با apiClient کار نمی‌کنند،
// همیشه از طریق همین توابع.
export const authApi = {
  login: (credentials) => apiClient.post('/auth/login', credentials),
  register: (data) => apiClient.post('/auth/register', data),
  // نکته: پروفایل کاربر توی یک router جدا (users.py) تعریف شده، نه auth.py
  getProfile: () => apiClient.get('/users/me'),
  logout: () => apiClient.post('/auth/logout'),
};

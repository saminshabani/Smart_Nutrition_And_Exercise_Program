import axios from 'axios';
import { ENV } from '@/config/env';

// یک نمونه واحد axios برای کل پروژه.
// همه‌ی api های feature ها (auth, workouts, nutrition, ...) از همین استفاده می‌کنند
// تا هدرها، مدیریت خطا و رفرش توکن در یک‌جا کنترل شود.
export const apiClient = axios.create({
  baseURL: ENV.API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// افزودن توکن به هر درخواست
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// مدیریت متمرکز خطاها (مثلاً خروج خودکار در صورت 401)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('accessToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

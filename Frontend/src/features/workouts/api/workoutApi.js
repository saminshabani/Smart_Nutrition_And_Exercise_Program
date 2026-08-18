import { apiClient } from '@/services/apiClient';

// فرض: router این بخش (app/routers/workout.py) با prefix="/workout" مانت شده،
// مثل الگوی auth.py -> /auth و users.py -> /users.
// اگر prefix واقعی فرق دارد، فقط همین دو مسیر را اصلاح کنید.
export const workoutApi = {
  // طبق منطق بک‌اند: اگر کاربر برنامه‌ی فعال (منقضی‌نشده) داشته باشد همان
  // برگردانده می‌شود، وگرنه یک برنامه‌ی جدید ساخته می‌شود. یعنی همین یک
  // تابع هم برای «گرفتن برنامه‌ی فعلی» و هم «ساخت برنامه‌ی جدید» کافی است.
  generateProgram: () => apiClient.post('/workout/generate'),
  deleteCurrentProgram: () => apiClient.delete('/workout/current'),
};

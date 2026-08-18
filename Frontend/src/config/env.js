// تمام مقادیر محیطی پروژه از یک نقطه خوانده می‌شوند
// تا در صورت تغییر، فقط همین فایل ویرایش شود.
export const ENV = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  IS_DEV: import.meta.env.DEV,
};

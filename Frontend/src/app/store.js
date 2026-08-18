import { configureStore } from '@reduxjs/toolkit';
import authReducer from '@/features/auth/authSlice';
import workoutsReducer from '@/features/workouts/workoutSlice';
import nutritionReducer from '@/features/nutrition/nutritionSlice';

// هر feature یک slice مستقل دارد و اینجا فقط ترکیب می‌شوند.
// برای افزودن یک feature جدید (مثلاً "progress")، کافیست:
// 1. src/features/progress/progressSlice.js را بسازید
// 2. اینجا import و اضافه کنید
export const store = configureStore({
  reducer: {
    auth: authReducer,
    workouts: workoutsReducer,
    nutrition: nutritionReducer,
  },
});

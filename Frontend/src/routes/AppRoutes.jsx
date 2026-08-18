import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { MainLayout } from '@/components/layout/MainLayout';
import { ProtectedRoute } from './ProtectedRoute';
import { Loader } from '@/components/common/Loader';

// صفحات به‌صورت lazy لود می‌شوند تا حجم اولیه‌ی باندل کم بماند.
// برای افزودن صفحه‌ی جدید فقط کافیست اینجا یک import و یک <Route> اضافه کنید.
const LandingPage = lazy(() =>
  import('@/features/landing/components/LandingPage').then((m) => ({ default: m.LandingPage }))
);
const LoginPage = lazy(() => import('@/features/auth/components/LoginForm').then((m) => ({ default: m.LoginForm })));
const SignupPage = lazy(() =>
  import('@/features/auth/components/SignupForm').then((m) => ({ default: m.SignupForm }))
);
const DashboardPage = lazy(() =>
  import('@/features/dashboard/components/DashboardPage').then((m) => ({ default: m.DashboardPage }))
);
const WorkoutList = lazy(() =>
  import('@/features/workouts/components/WorkoutList').then((m) => ({ default: m.WorkoutList }))
);
const MealPlanList = lazy(() =>
  import('@/features/nutrition/components/MealPlanList').then((m) => ({ default: m.MealPlanList }))
);

export function AppRoutes() {
  return (
    <Suspense fallback={<Loader />}>
      <Routes>
        <Route path="/" element={<LandingPage />} />

        <Route
          path="/login"
          element={
            <div className="h-screen flex items-center justify-center">
              <LoginPage />
            </div>
          }
        />

        <Route
          path="/signup"
          element={
            <div className="h-screen flex items-center justify-center">
              <SignupPage />
            </div>
          }
        />

        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/workouts" element={<WorkoutList />} />
          <Route path="/nutrition" element={<MealPlanList />} />
        </Route>
      </Routes>
    </Suspense>
  );
}

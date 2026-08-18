import { useNutrition } from '../hooks/useNutrition';
import { MealPlanCard } from './MealPlanCard';
import { Loader } from '@/components/common/Loader';

export function MealPlanList() {
  const { mealPlans, isLoading, error } = useNutrition();

  if (isLoading) return <Loader label="در حال بارگذاری برنامه‌های غذایی..." />;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {mealPlans.map((plan) => (
        <MealPlanCard key={plan.id} mealPlan={plan} />
      ))}
    </div>
  );
}

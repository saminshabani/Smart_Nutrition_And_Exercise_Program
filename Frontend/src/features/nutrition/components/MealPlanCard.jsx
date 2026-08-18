import { Card } from '@/components/common/Card';

export function MealPlanCard({ mealPlan }) {
  return (
    <Card className="flex flex-col gap-2">
      <h3 className="font-semibold text-gray-800">{mealPlan.title}</h3>
      <p className="text-sm text-gray-500">{mealPlan.description}</p>
      <div className="flex gap-2 text-xs text-gray-400">
        <span>{mealPlan.calories} کالری</span>
      </div>
    </Card>
  );
}

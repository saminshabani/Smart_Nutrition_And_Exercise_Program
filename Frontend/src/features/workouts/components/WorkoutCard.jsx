import { Card } from '@/components/common/Card';

export function WorkoutCard({ workout }) {
  return (
    <Card className="flex flex-col gap-2">
      <h3 className="font-semibold text-gray-800">{workout.title}</h3>
      <p className="text-sm text-gray-500">{workout.description}</p>
      <div className="flex gap-2 text-xs text-gray-400">
        <span>{workout.duration} دقیقه</span>
        <span>·</span>
        <span>{workout.level}</span>
      </div>
    </Card>
  );
}

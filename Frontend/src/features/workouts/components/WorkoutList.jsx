import { useState } from 'react';
import { ChevronDown, Play } from 'lucide-react';
import { useWorkoutProgram } from '../hooks/useWorkoutProgram';
import { Loader } from '@/components/common/Loader';
import { Button } from '@/components/common/Button';

// نام گروه عضلانی (target_muscle) از بک‌اند به‌صورت رشته‌ی خام می‌آید
// (مثل "chest"، "core"، "quads"). این نگاشت فقط برای نمایش یک برچسب
// فارسی خواناست؛ خود بک‌اند این دسته‌بندی را نگه نمی‌دارد.
// نام تمرین‌ها (chosen_exercise.name/instructions) از یک دیتاست عمومی
// می‌آیند و عمداً ترجمه نشده‌اند، چون ترجمه‌ی خودکار هزاران نام تمرین
// می‌تواند نادرست یا گمراه‌کننده باشد.
const MUSCLE_LABELS = {
  chest: 'سینه',
  back: 'پشت',
  shoulders: 'شانه',
  biceps: 'جلوبازو',
  triceps: 'پشت‌بازو',
  quads: 'جلوپا',
  hamstrings: 'همسترینگ',
  glutes: 'باسن',
  calves: 'ساق پا',
  abs: 'شکم',
  core: 'هسته‌ی بدن',
  forearms: 'ساعد',
  legs: 'پا',
  full_body: 'کل بدن',
};

function muscleLabel(target) {
  return MUSCLE_LABELS[target?.toLowerCase()] || target;
}

function repsLabel(slot) {
  if (slot.reps_min && slot.reps_max && slot.reps_min !== slot.reps_max) {
    return `${slot.reps_min} تا ${slot.reps_max} تکرار`;
  }
  return `${slot.reps_min ?? slot.reps_max ?? '-'} تکرار`;
}

function SlotRow({ slot }) {
  const [open, setOpen] = useState(false);
  const exercise = slot.chosen_exercise;

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between gap-3 p-4 text-start"
      >
        <div>
          <p className="text-xs font-bold tracking-wide text-rose-600 mb-1">{muscleLabel(slot.target_muscle)}</p>
          <p className="font-bold text-gray-900">{exercise?.name ?? 'تمرین نامشخص'}</p>
          <p className="text-sm text-gray-400 mt-0.5">
            {slot.sets ?? '-'} ست × {repsLabel(slot)}
          </p>
        </div>

        <span className="w-9 h-9 rounded-full bg-rose-50 text-rose-500 flex items-center justify-center shrink-0">
          {exercise?.instructions?.length ? (
            <ChevronDown size={16} className={`transition-transform ${open ? 'rotate-180' : ''}`} />
          ) : (
            <Play size={14} fill="currentColor" strokeWidth={0} />
          )}
        </span>
      </button>

      {open && exercise?.instructions?.length > 0 && (
        <div className="px-4 pb-4 -mt-1">
          <ol className="list-decimal list-inside text-sm text-gray-500 space-y-1 leading-relaxed">
            {exercise.instructions.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ol>
          {slot.rest_seconds != null && (
            <p className="text-xs text-gray-400 mt-2">استراحت بین ست‌ها: {slot.rest_seconds} ثانیه</p>
          )}
        </div>
      )}
    </div>
  );
}

export function WorkoutList() {
  const { program, isLoading, error } = useWorkoutProgram();
  const [selectedDay, setSelectedDay] = useState(0);

  if (isLoading) return <Loader label="در حال آماده‌سازی برنامه‌ی تمرینی..." />;

  if (error) {
    return (
      <div className="max-w-md mx-auto text-center py-12">
        <p className="text-gray-700 font-medium mb-1">نتونستیم برنامه‌ات رو بگیریم</p>
        <p className="text-sm text-gray-500">{error}</p>
      </div>
    );
  }

  if (!program) return null;

  const day = program.days[selectedDay];

  return (
    <div className="max-w-2xl mx-auto">
      {/* هدر — عنوان روز + زنگوله؛ زنگوله فقط دکوراتیو است */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <p className="text-xs font-bold tracking-wide text-gray-400 mb-1">برنامه‌ی تمرینی امروز</p>
          <h1 className="text-2xl font-extrabold text-gray-900">{day?.label ?? 'برنامه‌ی تمرینی'}</h1>
        </div>
      </div>

      {/* به‌جای آمار استریک/درصد تکمیل (که هنوز سمت بک‌اند نداریم)،
          یک جمله‌ی انگیزشی ثابت درباره‌ی ورزش نشان می‌دهیم. */}
      <div className="bg-gray-900 rounded-3xl p-6 mb-6">
        <p className="text-white font-bold leading-relaxed">
          «بدنت هر دردی که تحمل کنی رو تحمل می‌کنه؛ این ذهنته که باید متقاعدش کنی.»
        </p>
      </div>

      {/* اگر برنامه بیش از یک روز دارد، امکان جابه‌جایی بین روزها */}
      {program.days.length > 1 && (
        <div className="flex gap-2 mb-5 overflow-x-auto pb-1">
          {program.days.map((d, i) => (
            <button
              key={d.day_index}
              type="button"
              onClick={() => setSelectedDay(i)}
              className={`shrink-0 px-4 py-2 rounded-full text-sm font-semibold whitespace-nowrap transition ${
                i === selectedDay ? 'bg-gray-900 text-white' : 'bg-white text-gray-500 border border-gray-200'
              }`}
            >
              {d.label}
            </button>
          ))}
        </div>
      )}

      <h2 className="font-bold text-gray-900 mb-3">برنامه‌ی امروز</h2>

      <div className="flex flex-col gap-3 mb-6">
        {day?.slots.map((slot, i) => (
          <SlotRow key={i} slot={slot} />
        ))}
      </div>

      <Button variant="accent" className="w-full rounded-full text-base">
        شروع تمرین
      </Button>
    </div>
  );
}

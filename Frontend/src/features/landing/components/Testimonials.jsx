import { Star } from 'lucide-react';

// نظرات کاربران فعلاً محتوای نمونه (mock) هستند.
// به‌جای عکس واقعی افراد، از آواتار حرفی استفاده شده تا به یک فرد واقعی نسبت داده نشود.
// وقتی بک‌اند اندپوینت نظرات واقعی کاربران را داشت، این آرایه را با یک فراخوانی API جایگزین کنید.
const TESTIMONIALS = [
  {
    name: 'سارا جنکینز',
    role: 'طراح محصول',
    initials: 'سج',
    avatarColor: 'bg-primary-100 text-primary-700',
    quote:
      'برنامه‌های غذایی شخصی‌سازی‌شده فوق‌العاده ساده پیرویند. هر هفته ساعت‌ها در آماده‌سازی وعده‌ها صرفه‌جویی کردم و دقیقاً در بازه‌ی زمانی پیش‌بینی‌شده به وزن هدفم رسیدم.',
  },
  {
    name: 'دیوید چن',
    role: 'مهندس نرم‌افزار',
    initials: 'دچ',
    avatarColor: 'bg-amber-100 text-amber-700',
    quote:
      'فیت‌فیول کاملاً حدس‌وگمان را از برنامه‌ی تمرینی‌ام حذف کرد. راهنماهای وضعیت بدنی اختصاصی، امکان بازگشت ایمن به اسکوات‌های سنگین را برایم فراهم کرد.',
  },
  {
    name: 'النا روستوا',
    role: 'دونده‌ی ماراتن',
    initials: 'نر',
    avatarColor: 'bg-sky-100 text-sky-700',
    quote:
      'از وقتی به پروتکل زمان‌بندی پویای وعده‌های غذایی‌شان روی آوردم، متابولیسمم به‌شدت افزایش پیدا کرده. برای اولین بار در چند سال اخیر، اوج شفافیت ذهنی را تجربه می‌کنم.',
  },
];

export function Testimonials() {
  return (
    <section className="py-20">
      <div className="mx-auto max-w-6xl px-6">
        <div className="text-center mb-12">
          <span className="inline-block rounded-full bg-primary-100 text-primary-700 text-xs font-bold tracking-wide px-3 py-1.5 mb-5">
            داستان‌های موفقیت
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 leading-tight">
            محبوب در میان بیش از ۱۰٬۰۰۰ ورزشکار
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {TESTIMONIALS.map((t) => (
            <div key={t.name} className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col gap-4">
              <div className="flex gap-0.5 text-amber-400">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star key={i} size={16} fill="currentColor" strokeWidth={0} />
                ))}
              </div>

              <p className="text-sm text-gray-600 italic leading-relaxed">«{t.quote}»</p>

              <div className="flex items-center gap-3 mt-auto pt-2">
                <span
                  className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold shrink-0 ${t.avatarColor}`}
                >
                  {t.initials}
                </span>
                <div>
                  <p className="font-bold text-gray-900 text-sm">{t.name}</p>
                  <p className="text-xs text-gray-500">{t.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

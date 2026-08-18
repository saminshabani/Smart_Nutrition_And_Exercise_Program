import { Star } from 'lucide-react';

// این بخش نظرات مشتریان را نمایش می‌دهد.
// به‌جای عکس واقعی، آواتار حرف اول اسم را نشان می‌دهیم — هم ساده‌تر است
// هم نیازی به مدیریت فایل تصویر ندارد. وقتی سیستم نظرات واقعی از بک‌اند
// آماده شد، این آرایه را با نتیجه‌ی یک API جایگزین کنید.
const TESTIMONIALS = [
  {
    name: 'Sarah Jenkins',
    role: 'طراح محصول',
    quote:
      'برنامه‌های غذایی شخصی‌سازی‌شده فوق‌العاده ساده برای پیروی هستند. هر هفته ساعت‌ها در آماده‌سازی غذا صرفه‌جویی کردم و در بازه‌ی زمانی پیش‌بینی‌شده به وزن هدفم رسیدم.',
    avatarColor: 'bg-blue-100 text-blue-700',
  },
  {
    name: 'David Chen',
    role: 'مهندس نرم‌افزار',
    quote:
      'فیت‌فیول کاملاً حدس‌وگمان را از برنامه‌ی وزنه‌برداری من حذف کرد. راهنماهای اختصاصی وضعیت بدن به من اجازه داد با ایمنی کامل به اسکوات‌های سنگین برگردم.',
    avatarColor: 'bg-slate-200 text-slate-700',
  },
  {
    name: 'Elena Rostova',
    role: 'دونده‌ی ماراتن',
    quote:
      'از وقتی به پروتکل زمان‌بندی پویای غذایی آن‌ها روی آوردم، متابولیسمم به‌شدت افزایش یافته. برای اولین بار در چند سال اخیر، اوج شفافیت ذهنی را تجربه می‌کنم.',
    avatarColor: 'bg-cyan-100 text-cyan-700',
  },
];

export function TestimonialsSection() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="mx-auto max-w-6xl px-6">
        <div className="text-center mb-12">
          <span className="inline-block rounded-full bg-primary-100 text-primary-700 text-xs font-bold tracking-wide px-3 py-1.5 mb-5">
            داستان‌های موفقیت
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 leading-tight">
            مورد علاقه‌ی بیش از ۱۰٬۰۰۰ ورزشکار
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {TESTIMONIALS.map((t) => (
            <div key={t.name} className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col gap-4">
              <div className="flex gap-1 text-amber-400">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star key={i} size={16} fill="currentColor" strokeWidth={0} />
                ))}
              </div>

              <p className="text-gray-600 italic leading-relaxed">«{t.quote}»</p>

              <div className="flex items-center gap-3 mt-auto pt-2">
                <span
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm ${t.avatarColor}`}
                >
                  {t.name.charAt(0)}
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

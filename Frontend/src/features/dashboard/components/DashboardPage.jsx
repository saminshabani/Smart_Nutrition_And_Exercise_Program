import { Bell, Flame, Dumbbell, Leaf, User, ClipboardList, Quote, ArrowUpLeft } from 'lucide-react';

// این صفحه اولین چیزی است که کاربر بعد از ورود می‌بیند.
// در موبایل، هدر بالای صفحه و ناوبری Sidebar/Header اصلی (در MainLayout) مخفی می‌شوند
// و این صفحه هدر و پیمایش اختصاصی خودش (شبیه یک اپ موبایل) را نشان می‌دهد.
// در دسکتاپ، Header و Sidebar موجود در MainLayout همان نقش را ایفا می‌کنند
// و این صفحه فقط شبکه‌ی کارت‌ها را با اندازه‌ی بزرگ‌تر و در یک ردیف نشان می‌دهد.
//
// فعلاً محتوا mock است. وقتی بک‌اند اندپوینت مربوطه (وضعیت استریک، خلاصه‌ی
// تمرین/تغذیه‌ی امروز و ...) را داشت، این مقادیر باید از یک هوک (مثل
// الگوی features/workouts/hooks/useWorkouts) گرفته شوند.

const QUICK_LINKS = [
  {
    to: '/workouts',
    icon: Dumbbell,
    iconBg: 'bg-rose-100 text-rose-600',
    title: 'تمرین من',
    tag: 'روز بالاتنه',
    tagColor: 'text-rose-600',
    detail: 'امروز: سینه و پشت‌بازو',
  },
  {
    to: '/nutrition',
    icon: Leaf,
    iconBg: 'bg-teal-100 text-teal-600',
    title: 'تغذیه‌ی من',
    tag: 'سوخت‌رسانی به رشد',
    tagColor: 'text-teal-600',
    detail: '۱٬۲۰۰ کیلوکالری باقی‌مانده',
  },
  {
    to: '/profile',
    icon: User,
    iconBg: 'bg-violet-100 text-violet-600',
    title: 'پروفایل من',
    tag: 'پیگیری دستاوردها',
    tagColor: 'text-violet-600',
    detail: 'سطح: نخبه - سطح ۴',
  },
  {
    to: '/survey',
    icon: ClipboardList,
    iconBg: 'bg-amber-100 text-amber-600',
    title: 'نظرسنجی',
    tag: 'نظرت را به اشتراک بگذار',
    tagColor: 'text-amber-600',
    detail: '۵۰+ امتیاز XP جایزه بگیر',
  },
];

export function DashboardPage() {
  return (
    <div className="max-w-6xl mx-auto">
      {/* هدر مخصوص موبایل — در دسکتاپ Header اصلی این نقش را دارد */}
      <div className="sm:hidden flex items-start justify-between mb-6">
        <div>
          <p className="text-xs font-bold tracking-wide text-gray-400 mb-1">خوش آمدید، الکس</p>
          <h1 className="text-2xl font-extrabold text-gray-900">فیت‌فیول</h1>
        </div>
        <button
          type="button"
          aria-label="اعلان‌ها"
          className="w-10 h-10 rounded-full bg-white border border-gray-100 shadow-sm flex items-center justify-center text-gray-600"
        >
          <Bell size={18} />
        </button>
      </div>

      {/* کارت استریک هفتگی */}
      <div className="relative bg-gray-900 rounded-3xl p-6 mb-6 overflow-hidden">
        <span className="inline-flex items-center gap-1.5 bg-rose-500 text-white text-[11px] font-bold tracking-wide px-3 py-1 rounded-full mb-3">
          <Flame size={12} fill="currentColor" strokeWidth={0} />
          استریک هفتگی
        </span>
        <h2 className="text-xl font-extrabold text-white mb-1.5">شعله‌ی انگیزه‌ات را زنده نگه دار!</h2>
        <p className="text-sm text-gray-400 leading-relaxed max-w-md">
          ۵ روز متوالی است که ادامه می‌دهی. با تمرین بعدی، ۱۰۰ امتیاز XP جایزه می‌گیری.
        </p>
      </div>

      {/* شبکه‌ی کارت‌های میان‌بر — دو ستونه در موبایل، چهار ستونه و بزرگ‌تر در دسکتاپ */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        {QUICK_LINKS.map(({ to, icon: Icon, iconBg, title, tag, tagColor, detail }) => (
          <a
            key={to}
            href={to}
            className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 sm:p-6 flex flex-col gap-3 hover:shadow-md transition"
          >
            <div className="flex items-start justify-between">
              <span className={`w-10 h-10 sm:w-14 sm:h-14 rounded-xl sm:rounded-2xl flex items-center justify-center ${iconBg}`}>
                <Icon size={20} className="sm:hidden" />
                <Icon size={26} className="hidden sm:block" />
              </span>
              <ArrowUpLeft size={16} className="text-gray-300" />
            </div>
            <div>
              <h3 className="font-bold text-gray-900 text-sm sm:text-base">{title}</h3>
              <p className={`text-[11px] sm:text-xs font-bold ${tagColor} mt-0.5`}>{tag}</p>
              <p className="text-xs sm:text-sm text-gray-400 mt-1">{detail}</p>
            </div>
          </a>
        ))}
      </div>

      {/* نقل‌قول انگیزشی روزانه */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 flex items-center gap-3">
        <span className="w-9 h-9 rounded-xl bg-rose-100 text-rose-500 flex items-center justify-center shrink-0">
          <Quote size={16} fill="currentColor" strokeWidth={0} />
        </span>
        <p className="text-sm text-gray-600 italic leading-relaxed">
          «موفقیت همیشه درباره‌ی بزرگی نیست؛ درباره‌ی پایداری است.»
        </p>
      </div>
    </div>
  );
}

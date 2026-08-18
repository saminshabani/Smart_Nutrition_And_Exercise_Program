// این بخش سه مرحله‌ی واقعی و ترتیبی است (ثبت‌نام → هدف‌گذاری → دریافت برنامه)
// بنابراین استفاده از شماره‌گذاری اینجا معنادار است، نه صرفاً تزئینی.
//
// نکته: هر کارت فعلاً یک گرادیان جایگزین (placeholder) به‌جای تصویر/اسکرین‌شات دارد.
// وقتی اسکرین‌شات واقعی پنل کاربری یا عکس مرتبط آماده شد، همان <div> گرادیان را
// با <img src="..." className="w-full h-full object-cover" /> جایگزین کنید.
const STEPS = [
  {
    number: 1,
    title: 'ثبت‌نام کنید',
    description: 'پروفایل امن بدنی خود را با جزئیات وضعیت فعلی و اهداف اندازه‌گیری‌شده بسازید.',
    media: 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900',
    mediaLabel: 'تصویر پنل ساخت پروفایل',
  },
  {
    number: 2,
    title: 'هدف‌گذاری کنید',
    description: 'انتخاب کنید که به دنبال چربی‌سوزی سریع، عضله‌سازی خالص یا آماده‌سازی متابولیک تخصصی هستید.',
    media: 'bg-[radial-gradient(circle_at_center,theme(colors.amber.300),theme(colors.primary.600)_45%,theme(colors.slate.900)_85%)]',
    mediaLabel: 'تصویر انتخاب هدف',
  },
  {
    number: 3,
    title: 'برنامه‌تان را دریافت کنید',
    description: 'فهرست غذایی و برنامه‌ی تمرینی هفتگی‌تان، بلافاصله و مستقیم روی صفحه‌تان آماده می‌شود.',
    media: 'bg-gradient-to-br from-amber-50 via-stone-50 to-amber-100',
    mediaLabel: 'تصویر تحویل برنامه',
  },
];

export function StepsSection() {
  return (
    <section className="py-20">
      <div className="mx-auto max-w-6xl px-6">
        <div className="text-center mb-12">
          <span className="inline-block rounded-full bg-primary-100 text-primary-700 text-xs font-bold tracking-wide px-3 py-1.5 mb-5">
            پروتکل
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 leading-tight">
            سه گام ساده تا نشاط پایدار
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {STEPS.map((step) => (
            <div key={step.number} className="flex flex-col gap-4">
              <div className={`aspect-video rounded-2xl overflow-hidden flex items-center justify-center ${step.media}`}>
                <span className="text-xs text-white/50">{step.mediaLabel}</span>
              </div>

              <div className="flex items-center gap-2.5">
                <span className="w-6 h-6 shrink-0 rounded-full bg-primary-600 text-white text-xs font-bold flex items-center justify-center">
                  {step.number}
                </span>
                <h3 className="font-bold text-gray-900">{step.title}</h3>
              </div>

              <p className="text-sm text-gray-500 leading-relaxed">{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

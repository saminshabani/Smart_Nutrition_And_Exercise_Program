// این بخش پیش‌نمایش برنامه‌های تمرینی «فیت‌فیول» را نشان می‌دهد.
// فعلاً محتوا و تصاویر استاتیک (mock) هستند. وقتی بک‌اند اندپوینت
// مربوطه را داشت، این آرایه را با فراخوانی API (مثل الگوی
// features/workouts) جایگزین کنید.
//
// نکته: تصاویر فعلاً گرادیان جایگزین هستند؛ هرکدام را با
// <img src="..." className="w-full h-full object-cover" /> واقعی جایگزین کنید.
const PROGRAMS = [
  {
    category: 'آماده‌سازی بدنی',
    title: 'تمرینات HIIT برای مبتدیان',
    description:
      'از خستگی قلبی‌عروقی دور بمانید. پارامترهای پایه‌ی ریتم تمرین را یاد بگیرید که چربی‌سوزی را به حداکثر می‌رساند و در عین حال فیبرهای عضلانی را حفظ می‌کند.',
    media: 'bg-gradient-to-br from-slate-800 via-slate-900 to-black',
  },
  {
    category: 'قدرت و وزنه‌برداری',
    title: 'مبانی تمرین قدرتی',
    description:
      'فرم حرکت همه‌چیز است. حالت‌های مکانیکی اصلی ددلیفت و اسکوات را بشناسید تا زنجیره‌های حرکتی را با بیشترین ایمنی بارگذاری کنید.',
    media: 'bg-gradient-to-br from-zinc-800 via-neutral-900 to-black',
  },
  {
    category: 'تحرک‌پذیری',
    title: 'برنامه‌های کششی',
    description:
      'باز کردن دامنه‌های محدودشده‌ی حرکتی. چرا تحرک‌بخشی روزانه‌ی همسترینگ و ستون فقرات سینه‌ای مستقیماً به افزایش رکوردهای وزنه‌برداری منجر می‌شود.',
    media: 'bg-gradient-to-br from-amber-900 via-stone-800 to-neutral-900',
  },
];

export function WorkoutPrograms() {
  return (
    <section className="py-20 bg-[#0B1120]">
      <div className="mx-auto max-w-6xl px-6">
        <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-6 mb-12">
          <div>
            <span className="inline-block rounded-full bg-primary-500/20 text-primary-400 text-xs font-bold tracking-wide px-3 py-1.5 mb-4">
              آکادمی ورزشی فیت‌فیول
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white leading-tight">
              قدرت بسازید، فرم حرکات را اصلاح کنید
            </h2>
          </div>

          <a
            href="/workouts"
            className="shrink-0 rounded-full bg-primary-500 text-white text-sm font-semibold px-5 py-3 text-center hover:bg-primary-600 transition"
          >
            همه‌ی برنامه‌های تمرینی
          </a>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {PROGRAMS.map((program) => (
            <article
              key={program.title}
              className="bg-white/5 rounded-2xl border border-white/10 overflow-hidden"
            >
              <div className={`aspect-[4/3] ${program.media}`} />

              <div className="p-5 flex flex-col gap-2">
                <span className="text-xs font-bold tracking-wide text-primary-400">{program.category}</span>
                <h3 className="font-bold text-white">{program.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed">{program.description}</p>
                <a
                  href="/workouts"
                  className="text-sm font-semibold text-white underline underline-offset-4 mt-2 w-fit"
                >
                  تماشای ویدیوی تکنیک
                </a>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

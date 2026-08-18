// این بخش پیش‌نمایش مقالات «آشپزخانه فیت‌فیول» را نشان می‌دهد.
// فعلاً محتوا و تصاویر استاتیک (mock) هستند. وقتی بک‌اند یک اندپوینت
// برای مقالات داشت، این آرایه را با یک فراخوانی API (مثل الگوی
// features/workouts) جایگزین کنید.
//
// نکته: تصاویر غذا فعلاً گرادیان جایگزین هستند؛ هرکدام را با
// <img src="..." className="w-full h-full object-cover" /> واقعی جایگزین کنید.
const GUIDES = [
  {
    category: 'علم صبحانه',
    title: 'صبح‌هایتان را درست تغذیه کنید',
    description:
      'بدانید چرا مصرف کربوهیدرات‌های پیچیده در همان ابتدای صبح از افزایش ناگهانی کورتیزول جلوگیری می‌کند و انرژی پایدار را برای ساعت‌ها حفظ می‌کند.',
    media: 'bg-gradient-to-br from-amber-100 via-orange-50 to-amber-200',
  },
  {
    category: 'وعده‌های ریکاوری',
    title: 'وعده‌های غذایی پس از تمرین',
    description:
      'بهینه‌سازی سنتز پروتئین با نسبت ایده‌آل ۳ به ۱ کربوهیدرات به پروتئین؛ علم پشت ترمیم پارگی‌های سلولی پس از تمرین قدرتی.',
    media: 'bg-gradient-to-br from-orange-200 via-rose-100 to-orange-300',
  },
  {
    category: 'آب‌رسانی',
    title: 'عادت‌های آب‌رسانی',
    description:
      'آب چیزی فراتر از رفع تشنگی است. بیاموزید چگونه تأمین الکترولیت و زمان‌بندی بهینه، نرخ متابولیسم را تا ۳۰٪ افزایش می‌دهد.',
    media: 'bg-gradient-to-br from-sky-50 via-cyan-50 to-sky-100',
  },
];

export function NutritionGuides() {
  return (
    <section className="py-20 bg-[#FAF7F0]">
      <div className="mx-auto max-w-6xl px-6">
        <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-6 mb-12">
          <div>
            <span className="inline-block rounded-full bg-primary-100 text-primary-700 text-xs font-bold tracking-wide px-3 py-1.5 mb-4">
              آشپزخانه فیت‌فیول
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 leading-tight">
              بدن خود را آگاهانه تغذیه کنید
            </h2>
          </div>

          <a
            href="/nutrition/guides"
            className="shrink-0 rounded-full bg-primary-600 text-white text-sm font-semibold px-5 py-3 text-center hover:bg-primary-700 transition"
          >
            همه‌ی راهنماهای تغذیه
          </a>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {GUIDES.map((guide) => (
            <article key={guide.title} className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
              <div className={`aspect-[4/3] ${guide.media}`} />

              <div className="p-5 flex flex-col gap-2">
                <span className="text-xs font-bold tracking-wide text-primary-600">{guide.category}</span>
                <h3 className="font-bold text-gray-900">{guide.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{guide.description}</p>
                <a
                  href="/nutrition/guides"
                  className="text-sm font-semibold text-gray-900 underline underline-offset-4 mt-2 w-fit"
                >
                  مطالعه‌ی راهنمای کامل
                </a>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

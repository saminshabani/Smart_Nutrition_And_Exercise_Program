import { Apple, Dumbbell, LineChart } from 'lucide-react';

// این بخش زیر Hero قرار می‌گیرد و سه ویژگی اصلی محصول را معرفی می‌کند.
// آیکون‌ها از lucide-react هستند — بعد از افزودن این فایل حتماً یک‌بار
// npm install اجرا کنید تا پکیج نصب شود.
const FEATURES = [
  {
    icon: Apple,
    title: 'برنامه‌های غذایی شخصی‌سازی‌شده',
    description:
      'راهنمای پویای آشپزخانه، دقیقاً متناسب با اهداف کالری، نسبت درشت‌مغذی‌ها و ترجیحات زیستی مواد غذایی شما.',
  },
  {
    icon: Dumbbell,
    title: 'برنامه‌های تمرینی اختصاصی',
    description:
      'بلوک‌های تمرینی ماژولار، متناسب با تجهیزات در دسترس، محدودیت‌های وضعیت بدنی و سرعت ریکاوری شما.',
  },
  {
    icon: LineChart,
    title: 'پایش لحظه‌ای پیشرفت',
    description:
      'همگام‌سازی مداوم داده‌ها که حجم تمرینات و شاخص‌های وزنی را به به‌روزرسانی‌های عملی در جدول زمانی تبدیل می‌کند.',
  },
];

export function FeatureGrid() {
  return (
    <section className="bg-gray-50 py-20">
      <div className="mx-auto max-w-6xl px-6">
        <div className="text-center mb-12">
          <span className="inline-block rounded-full bg-primary-100 text-primary-700 text-xs font-bold tracking-wide px-3 py-1.5 mb-5">
            مزیت بی‌رقیب
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 leading-tight">
            معماری علمی برای سلامتی شما
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {FEATURES.map(({ icon: Icon, title, description }) => (
            <div
              key={title}
              className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col items-start gap-4"
            >
              <span className="w-11 h-11 rounded-xl bg-primary-100 text-primary-600 flex items-center justify-center">
                <Icon size={22} strokeWidth={2} />
              </span>
              <div>
                <h3 className="font-bold text-gray-900 mb-1.5">{title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

import { Zap, Instagram, Twitter, Youtube, Facebook } from 'lucide-react';

// فوتر سراسری سایت. فعلاً فقط در LandingPage استفاده می‌شود؛
// اگر خواستید در صفحات داخلی (بعد از لاگین) هم نمایش داده شود،
// آن را به MainLayout هم اضافه کنید.
const LINK_COLUMNS = [
  {
    title: 'شرکت',
    links: ['درباره‌ی ما', 'علم ما', 'رسانه', 'فرصت‌های شغلی'],
  },
  {
    title: 'راهکارها',
    links: ['برنامه‌های غذایی', 'برنامه‌های تمرینی', 'اسکن آناتومی', 'قیمت‌گذاری'],
  },
  {
    title: 'منابع',
    links: ['راهنماهای وبلاگ', 'ابزارهای محاسبه', 'مرکز پشتیبانی', 'توسعه‌دهندگان'],
  },
];

const SOCIALS = [
  { icon: Instagram, label: 'اینستاگرام' },
  { icon: Twitter, label: 'ایکس' },
  { icon: Youtube, label: 'یوتیوب' },
  { icon: Facebook, label: 'فیسبوک' },
];

export function Footer() {
  return (
    <footer className="bg-gray-50 border-t border-gray-100">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-[1.4fr,1fr,1fr,1fr] gap-10">
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded-lg bg-primary-600 text-white flex items-center justify-center">
                <Zap size={16} fill="currentColor" strokeWidth={0} />
              </span>
              <span className="font-extrabold text-gray-900">فیت‌فیول</span>
            </div>
            <p className="text-sm text-gray-500 leading-relaxed max-w-xs">
              طراحی مهندسی‌شده‌ی تناسب‌اندام ماژولار و نقشه‌برداری زیستی تغذیه. بازتعریف روزانه‌ی توان بدنی
              فعال.
            </p>
          </div>

          {LINK_COLUMNS.map((column) => (
            <div key={column.title}>
              <h4 className="font-bold text-gray-900 mb-4 text-sm">{column.title}</h4>
              <ul className="flex flex-col gap-3">
                {column.links.map((link) => (
                  <li key={link}>
                    <a href="#" className="text-sm text-gray-500 hover:text-gray-900 transition">
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-10 mt-10 border-t border-gray-200">
          <p className="text-xs text-gray-400">© ۲۰۲۶ فیت‌فیول. تمامی حقوق محفوظ است. نرم‌افزار سلامت دقیق.</p>
          <div className="flex items-center gap-2">
            {SOCIALS.map(({ icon: Icon, label }) => (
              <a
                key={label}
                href="#"
                aria-label={label}
                className="w-8 h-8 rounded-full bg-white border border-gray-200 text-gray-500 flex items-center justify-center hover:text-gray-900 transition"
              >
                <Icon size={14} />
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}

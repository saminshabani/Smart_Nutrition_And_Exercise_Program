import { Link } from 'react-router-dom';

// این کامپوننت اولین چیزی است که کاربر مهمان (قبل از ثبت‌نام) می‌بیند.
// طبق طرح ارائه‌شده پیاده‌سازی شده و به فارسی و راست‌به‌چپ برگردانده شده.
//
// نکته: تصویر فعلاً یک گرادیان جایگزین (placeholder) است.
// عکس واقعی وعده‌های غذایی را در src/assets/images بگذارید و
// در پایین همین فایل، بخش «تصویر وعده‌ی غذایی» را با <img src={...} /> جایگزین کنید.
export function LandingHero() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-16 sm:py-24">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        {/* ستون متن — در RTL سمت راست قرار می‌گیرد */}
        <div className="flex flex-col items-start gap-6">
          <span className="inline-block rounded-full bg-primary-100 text-primary-700 text-xs font-bold tracking-wide px-3 py-1.5">
            شخصی‌سازی ویژه
          </span>

          <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 leading-tight">
            مسیر اختصاصی شما
            <br />
            به سوی تناسب‌اندام و تغذیه
          </h1>

          <p className="text-gray-500 text-lg leading-relaxed max-w-md">
            فیت‌فیول برنامه‌های غذایی و تمرینی را دقیقاً متناسب با بدن، برنامه‌ی
            روزانه و اهداف عملکردی شما طراحی می‌کند. نه توصیه‌های کلی و یکسان
            برای همه؛ فقط نتیجه.
          </p>

          <Link
            to="/signup"
            className="rounded-full border-2 border-gray-900 px-7 py-3 font-semibold text-gray-900 transition hover:bg-gray-900 hover:text-white"
          >
            مشاهده‌ی برنامه‌ها
          </Link>

          <div className="flex items-center gap-8 pt-6 mt-2 border-t border-gray-200 w-full">
            <div>
              <p className="text-3xl font-extrabold text-gray-900">٪۹۸</p>
              <p className="text-sm text-gray-500">نرخ موفقیت</p>
            </div>
            <div>
              <p className="text-3xl font-extrabold text-gray-900">+۱۵۰هزار</p>
              <p className="text-sm text-gray-500">برنامه‌ی فعال ساخته‌شده</p>
            </div>
          </div>
        </div>

        {/* ستون تصویر */}
        <div className="relative aspect-square rounded-[2rem] overflow-hidden shadow-xl bg-gradient-to-br from-primary-100 via-amber-50 to-primary-50">
          {/* تصویر وعده‌ی غذایی — با <img src="/src/assets/images/meal-prep.jpg" ... /> جایگزین شود */}
          <div className="absolute inset-0 flex items-center justify-center text-primary-700/40 text-sm">
            تصویر وعده‌های غذایی اینجا قرار می‌گیرد
          </div>

          <div className="absolute bottom-6 inset-x-6 bg-white rounded-2xl shadow-lg px-4 py-3 flex items-center gap-3">
            <span className="w-9 h-9 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center text-lg">
              🔥
            </span>
            <div>
              <p className="text-[11px] font-semibold tracking-wide text-gray-400">
                سوزاننده‌ی فعال
              </p>
              <p className="text-sm font-bold text-gray-900">
                هدف ۶۵۰ کیلوکالری محقق شد
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

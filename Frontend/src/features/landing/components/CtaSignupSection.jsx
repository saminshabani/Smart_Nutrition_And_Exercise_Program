import { Check } from 'lucide-react';
import { SignupForm } from '@/features/auth/components/SignupForm';

const CHECKLIST = [
  'محاسبات درشت‌مغذی ۱۰۰٪ شخصی‌سازی‌شده',
  'چرخه‌های تمرینی و بلوک‌های پیشگیری از آسیب، طراحی‌شده توسط متخصصان',
  'چک‌این هفتگی مستقیم با مربی',
];

export function CtaSignupSection() {
  return (
    <section className="py-20">
      <div className="mx-auto max-w-6xl px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="flex flex-col items-start gap-5">
            <span className="inline-block rounded-full bg-primary-100 text-primary-700 text-xs font-bold tracking-wide px-3 py-1.5">
              سفرتان را آغاز کنید
            </span>

            <h2 className="text-4xl font-extrabold text-gray-900 leading-tight">
              امروز، خط پایه‌ی بدنی‌تان را متحول کنید
            </h2>

            <p className="text-gray-500 text-lg leading-relaxed max-w-md">
              به جمع ما بپیوندید. پروفایل بدنی خود را در کمتر از ۳ دقیقه بسازید، اهداف دقیق جسمی‌تان را تعیین
              کنید و بگذارید موتور ما اولین نقشه‌ی راه پرفورمنس شما را طراحی کند.
            </p>

            <ul className="flex flex-col gap-3 mt-2">
              {CHECKLIST.map((item) => (
                <li key={item} className="flex items-center gap-2.5 text-sm text-gray-700">
                  <span className="w-5 h-5 shrink-0 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center">
                    <Check size={12} strokeWidth={3} />
                  </span>
                  {item}
                </li>
              ))}
            </ul>
          </div>

          <div className="flex justify-center lg:justify-start">
            <SignupForm />
          </div>
        </div>
      </div>
    </section>
  );
}

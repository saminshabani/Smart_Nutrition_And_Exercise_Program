import { Check } from 'lucide-react';
import { SignupForm } from '@/features/auth/components/SignupForm';

const BENEFITS = [
  'محاسبات درشت‌مغذی ۱۰۰٪ شخصی‌سازی‌شده',
  'چرخه‌های تمرینی و بلوک‌های پیشگیری از آسیب طراحی‌شده توسط متخصصان',
  'چک-این هفتگی مستقیم با مربی',
];

export function SignupCTA() {
  return (
    <section className="py-20">
      <div className="mx-auto max-w-6xl px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          <div className="flex flex-col items-start gap-6">
            <span className="inline-block rounded-full bg-primary-100 text-primary-700 text-xs font-bold tracking-wide px-3 py-1.5">
              آغاز مسیر شما
            </span>

            <h2 className="text-3xl sm:text-4xl font-extrabold text-gray-900 leading-tight">
              همین امروز نقطه‌ی شروع بدنتان را دگرگون کنید
            </h2>

            <p className="text-gray-500 text-lg leading-relaxed max-w-md">
              به این مجموعه بپیوندید. پروفایل بدنی خود را در کمتر از ۳ دقیقه بسازید، اهداف دقیق جسمی‌تان را
              تعیین کنید و بگذارید موتور ما اولین نقشه‌ی راه پرقدرت شما را طراحی کند.
            </p>

            <ul className="flex flex-col gap-3">
              {BENEFITS.map((benefit) => (
                <li key={benefit} className="flex items-center gap-2.5 text-sm text-gray-700">
                  <span className="w-5 h-5 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center shrink-0">
                    <Check size={13} strokeWidth={3} />
                  </span>
                  {benefit}
                </li>
              ))}
            </ul>
          </div>

          <div className="flex justify-center lg:justify-end">
            <SignupForm />
          </div>
        </div>
      </div>
    </section>
  );
}

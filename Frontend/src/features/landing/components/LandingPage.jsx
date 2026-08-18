import { LandingHero } from './LandingHero';
import { FeatureGrid } from './FeatureGrid';
import { StepsSection } from './StepsSection';
import { NutritionGuides } from './NutritionGuides';
import { WorkoutPrograms } from './WorkoutPrograms';
import { Testimonials } from './Testimonials';
import { SignupCTA } from './SignupCTA';
import { Footer } from '@/components/layout/Footer';

// صفحه‌ی عمومی اصلی سایت (قبل از ثبت‌نام/ورود).
// اگر بعداً بخش جدیدی اضافه شد، آن را در همین پوشه به‌صورت یک کامپوننت
// جدا بسازید و اینجا زیر بخش‌های موجود بچینید (Footer همیشه آخرین چیز است).
export function LandingPage() {
  return (
    <div className="bg-white">
      <LandingHero />
      <FeatureGrid />
      <StepsSection />
      <NutritionGuides />
      <WorkoutPrograms />
      <Testimonials />
      <SignupCTA />
      <Footer />
    </div>
  );
}

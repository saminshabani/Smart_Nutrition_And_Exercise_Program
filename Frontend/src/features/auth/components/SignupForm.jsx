import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Input } from '@/components/common/Input';
import { Button } from '@/components/common/Button';

export function SignupForm() {
  const { register: registerUser, login, isLoading, error } = useAuth();
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  // بک‌اند شما بعد از ثبت‌نام توکن برنمی‌گرداند (فقط اطلاعات کاربر می‌سازد)،
  // پس برای تجربه‌ی کاربری روان، بلافاصله بعد از ثبت‌نام موفق، با همان
  // ایمیل/رمز عبور یک لاگین خودکار هم انجام می‌دهیم.
  const onSubmit = async (values) => {
    const registerResult = await registerUser(values);
    if (registerResult.error) return;

    const loginResult = await login({ email: values.email, password: values.password });
    if (!loginResult.error) navigate('/dashboard');
  };

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 sm:p-8 w-full max-w-md">
      <h3 className="text-xl font-bold text-gray-900 mb-1">ساخت حساب کاربری</h3>
      <p className="text-sm text-gray-500 mb-6">با ۱۴ روز آزمایشی پرمیوم شروع کنید، بدون نیاز به کارت اعتباری.</p>

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
        <Input
          label="نام کاربری"
          type="text"
          placeholder="ali_moradi"
          error={errors.username?.message}
          {...register('username', { required: 'نام کاربری الزامی است' })}
        />
        <Input
          label="آدرس ایمیل"
          type="email"
          placeholder="you@example.com"
          error={errors.email?.message}
          {...register('email', { required: 'ایمیل الزامی است' })}
        />
        <Input
          label="رمز عبور"
          type="password"
          placeholder="یک رمز عبور امن انتخاب کنید"
          error={errors.password?.message}
          {...register('password', {
            required: 'رمز عبور الزامی است',
            minLength: { value: 8, message: 'رمز عبور باید حداقل ۸ کاراکتر باشد' },
          })}
        />

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <Button type="submit" loading={isLoading} className="w-full mt-2">
          همین حالا ثبت‌نام کنید
        </Button>

        <p className="text-center text-sm text-gray-500">
          قبلاً حساب کاربری دارید؟{' '}
          <a href="/login" className="text-primary-600 font-semibold hover:underline">
            ورود
          </a>
        </p>
      </form>
    </div>
  );
}

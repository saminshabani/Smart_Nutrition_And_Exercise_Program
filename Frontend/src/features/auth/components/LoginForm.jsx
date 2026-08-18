import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Input } from '@/components/common/Input';
import { Button } from '@/components/common/Button';

export function LoginForm() {
  const { login, isLoading, error } = useAuth();
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async (values) => {
    const result = await login(values);
    if (!result.error) navigate('/dashboard');
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 max-w-sm w-full">
      <Input
        label="ایمیل"
        type="email"
        error={errors.email?.message}
        {...register('email', { required: 'ایمیل الزامی است' })}
      />
      <Input
        label="رمز عبور"
        type="password"
        error={errors.password?.message}
        {...register('password', { required: 'رمز عبور الزامی است' })}
      />
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <Button type="submit" loading={isLoading}>
        ورود
      </Button>
    </form>
  );
}

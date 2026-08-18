import { useAuth } from '@/features/auth/hooks/useAuth';
import { Button } from '@/components/common/Button';

export function Header() {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <header className="hidden sm:flex h-16 items-center justify-between px-6 border-b bg-white">
      <span className="font-bold text-lg text-primary-700">برنامه ورزشی و غذایی</span>
      {isAuthenticated && (
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-600">سلام، {user?.username}</span>
          <Button variant="outline" onClick={logout}>
            خروج
          </Button>
        </div>
      )}
    </header>
  );
}

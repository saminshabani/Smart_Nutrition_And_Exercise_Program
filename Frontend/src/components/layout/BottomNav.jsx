import { NavLink } from 'react-router-dom';
import { Home, Dumbbell, Leaf, User } from 'lucide-react';

// این نوار فقط زیر breakpointsm نمایش داده می‌شود (معادل موبایل).
// در دسکتاپ، Sidebar موجود در components/layout همین نقش را ایفا می‌کند.
const TABS = [
  { to: '/dashboard', label: 'خانه', icon: Home },
  { to: '/workouts', label: 'تمرین', icon: Dumbbell },
  { to: '/nutrition', label: 'تغذیه', icon: Leaf },
  { to: '/profile', label: 'پروفایل', icon: User },
];

export function BottomNav() {
  return (
    <nav className="sm:hidden fixed bottom-0 inset-x-0 bg-white border-t border-gray-100 flex items-center justify-around py-2 z-10">
      {TABS.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) =>
            `flex flex-col items-center gap-1 px-4 py-1 text-xs font-medium ${
              isActive ? 'text-primary-600' : 'text-gray-400'
            }`
          }
        >
          <Icon size={20} strokeWidth={2} />
          {label}
        </NavLink>
      ))}
    </nav>
  );
}

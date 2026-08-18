import { NavLink } from 'react-router-dom';

const links = [
  { to: '/dashboard', label: 'داشبورد' },
  { to: '/workouts', label: 'برنامه ورزشی' },
  { to: '/nutrition', label: 'برنامه غذایی' },
  { to: '/profile', label: 'پروفایل' },
];

export function Sidebar() {
  return (
    <aside className="hidden sm:flex sm:flex-col w-56 border-l bg-white h-full p-4 gap-1">
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          className={({ isActive }) =>
            `px-3 py-2 rounded-lg text-sm ${
              isActive ? 'bg-primary-50 text-primary-700 font-medium' : 'text-gray-600 hover:bg-gray-50'
            }`
          }
        >
          {link.label}
        </NavLink>
      ))}
    </aside>
  );
}

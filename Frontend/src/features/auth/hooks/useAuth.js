import { useSelector, useDispatch } from 'react-redux';
import { login, register, logout } from '../authSlice';

// این هوک تنها راهی است که بقیه‌ی اپ باید با state احراز هویت کار کند.
// کامپوننت‌ها نباید مستقیم useSelector روی state.auth بزنند.
export function useAuth() {
  const dispatch = useDispatch();
  const { user, status, error } = useSelector((state) => state.auth);

  return {
    user,
    isAuthenticated: Boolean(user),
    isLoading: status === 'loading',
    error,
    login: (credentials) => dispatch(login(credentials)),
    register: (payload) => dispatch(register(payload)),
    logout: () => dispatch(logout()),
  };
}

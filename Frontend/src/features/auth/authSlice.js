import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { authApi } from './api/authApi';

// نکته‌ی مهم: بک‌اند FastAPI شما در پاسخ لاگین فقط access_token برمی‌گرداند،
// نه اطلاعات کاربر. به همین دلیل بلافاصله بعد از لاگین یک درخواست جدا
// به /auth/me می‌زنیم تا پروفایل کاربر را بگیریم.
export const login = createAsyncThunk('auth/login', async (credentials, { rejectWithValue }) => {
  try {
    const { data } = await authApi.login(credentials);
    localStorage.setItem('accessToken', data.access_token);

    const profileRes = await authApi.getProfile();
    return profileRes.data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.detail || 'خطا در ورود');
  }
});

// نکته‌ی مهم: /auth/register در بک‌اند شما فقط اطلاعات کاربر ساخته‌شده را
// برمی‌گرداند (بدون توکن)، یعنی کاربر بعد از ثبت‌نام هنوز لاگین نشده.
// کامپوننت SignupForm بعد از موفقیت این thunk، خودش login را هم صدا می‌زند.
export const register = createAsyncThunk('auth/register', async (payload, { rejectWithValue }) => {
  try {
    const { data } = await authApi.register(payload);
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.detail || 'خطا در ثبت‌نام');
  }
});

export const fetchProfile = createAsyncThunk('auth/fetchProfile', async (_, { rejectWithValue }) => {
  try {
    const { data } = await authApi.getProfile();
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.detail || 'خطا در دریافت پروفایل');
  }
});

const initialState = {
  user: null,
  status: 'idle', // idle | loading | succeeded | failed
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      localStorage.removeItem('accessToken');
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.user = action.payload;
      })
      .addCase(login.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      })
      .addCase(register.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(register.fulfilled, (state) => {
        // کاربر هنوز لاگین نشده (توکنی در کار نیست)، پس state.user را ست نمی‌کنیم.
        state.status = 'succeeded';
      })
      .addCase(register.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      })
      .addCase(fetchProfile.fulfilled, (state, action) => {
        state.user = action.payload;
      });
  },
});

export const { logout } = authSlice.actions;
export default authSlice.reducer;

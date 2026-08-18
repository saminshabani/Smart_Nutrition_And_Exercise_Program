import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { workoutApi } from './api/workoutApi';

// این thunk هم «گرفتن برنامه‌ی فعلی» و هم «ساخت برنامه‌ی جدید در صورت نبود»
// را با هم انجام می‌دهد (منطقش سمت بک‌اند است).
export const fetchOrGenerateProgram = createAsyncThunk(
  'workouts/generate',
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await workoutApi.generateProgram();
      return data;
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'خطا در دریافت برنامه‌ی تمرینی');
    }
  }
);

export const deleteCurrentProgram = createAsyncThunk(
  'workouts/deleteCurrent',
  async (_, { rejectWithValue }) => {
    try {
      await workoutApi.deleteCurrentProgram();
    } catch (err) {
      return rejectWithValue(err.response?.data?.detail || 'خطا در حذف برنامه‌ی تمرینی');
    }
  }
);

const workoutSlice = createSlice({
  name: 'workouts',
  initialState: {
    program: null, // شکل آن دقیقاً WorkoutProgramOut از بک‌اند است
    status: 'idle', // idle | loading | succeeded | failed
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchOrGenerateProgram.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(fetchOrGenerateProgram.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.program = action.payload;
      })
      .addCase(fetchOrGenerateProgram.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      })
      .addCase(deleteCurrentProgram.fulfilled, (state) => {
        state.program = null;
        state.status = 'idle';
      });
  },
});

export default workoutSlice.reducer;

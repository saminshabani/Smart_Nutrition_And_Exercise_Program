import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { nutritionApi } from './api/nutritionApi';

export const fetchMealPlans = createAsyncThunk('nutrition/fetchAll', async (_, { rejectWithValue }) => {
  try {
    const { data } = await nutritionApi.getMealPlans();
    return data;
  } catch (err) {
    return rejectWithValue(err.response?.data?.detail || 'خطا در دریافت برنامه‌های غذایی');
  }
});

const nutritionSlice = createSlice({
  name: 'nutrition',
  initialState: { items: [], status: 'idle', error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchMealPlans.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchMealPlans.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload;
      })
      .addCase(fetchMealPlans.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload;
      });
  },
});

export default nutritionSlice.reducer;

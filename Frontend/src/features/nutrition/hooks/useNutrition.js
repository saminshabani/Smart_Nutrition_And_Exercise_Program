import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchMealPlans } from '../nutritionSlice';

export function useNutrition() {
  const dispatch = useDispatch();
  const { items, status, error } = useSelector((state) => state.nutrition);

  useEffect(() => {
    if (status === 'idle') dispatch(fetchMealPlans());
  }, [status, dispatch]);

  return { mealPlans: items, isLoading: status === 'loading', error };
}

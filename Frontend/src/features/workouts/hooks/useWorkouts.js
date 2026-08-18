import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchWorkouts } from '../workoutSlice';

export function useWorkouts() {
  const dispatch = useDispatch();
  const { items, status, error } = useSelector((state) => state.workouts);

  useEffect(() => {
    if (status === 'idle') dispatch(fetchWorkouts());
  }, [status, dispatch]);

  return { workouts: items, isLoading: status === 'loading', error };
}

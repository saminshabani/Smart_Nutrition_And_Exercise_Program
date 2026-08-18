import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchOrGenerateProgram } from '../workoutSlice';

export function useWorkoutProgram() {
  const dispatch = useDispatch();
  const { program, status, error } = useSelector((state) => state.workouts);

  useEffect(() => {
    if (status === 'idle') dispatch(fetchOrGenerateProgram());
  }, [status, dispatch]);

  return { program, isLoading: status === 'loading', error };
}

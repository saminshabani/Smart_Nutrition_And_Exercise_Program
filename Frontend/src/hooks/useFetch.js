import { useEffect, useState, useCallback } from 'react';

// هوک عمومی برای درخواست‌های ساده‌ای که نیاز به redux ندارند
// (مثلاً داده‌های یک‌بار مصرف در یک صفحه‌ی خاص).
export function useFetch(fetchFn, deps = []) {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const run = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await fetchFn();
      setData(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'خطایی رخ داد');
    } finally {
      setIsLoading(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    run();
  }, [run]);

  return { data, isLoading, error, refetch: run };
}

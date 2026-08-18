import { forwardRef } from 'react';

export const Input = forwardRef(function Input({ label, error, ...props }, ref) {
  return (
    <label className="flex flex-col gap-1 text-sm">
      {label && <span className="text-gray-700">{label}</span>}
      <input
        ref={ref}
        className={`px-3 py-2 rounded-lg border outline-none focus:ring-2 focus:ring-primary-500 ${
          error ? 'border-red-500' : 'border-gray-300'
        }`}
        {...props}
      />
      {error && <span className="text-red-500 text-xs">{error}</span>}
    </label>
  );
});

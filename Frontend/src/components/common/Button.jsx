export function Button({ children, loading, variant = 'primary', className = '', ...props }) {
  const base = 'px-4 py-2 rounded-xl font-medium transition disabled:opacity-60 disabled:cursor-not-allowed';
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700',
    secondary: 'bg-gray-100 text-gray-800 hover:bg-gray-200',
    outline: 'border border-primary-600 text-primary-600 hover:bg-primary-50',
    accent: 'bg-rose-500 text-white hover:bg-rose-600',
  };

  return (
    <button className={`${base} ${variants[variant]} ${className}`} disabled={loading} {...props}>
      {loading ? 'در حال پردازش...' : children}
    </button>
  );
}

export function Loader({ label = 'در حال بارگذاری...' }) {
  return (
    <div className="flex items-center justify-center gap-2 py-8 text-gray-500">
      <span className="w-5 h-5 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      <span>{label}</span>
    </div>
  );
}

export function formatNumber(value) {
  return new Intl.NumberFormat('fa-IR').format(value);
}

export function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

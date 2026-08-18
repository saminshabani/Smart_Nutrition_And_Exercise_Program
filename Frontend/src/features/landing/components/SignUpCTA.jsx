import React, { useState } from 'react';

export default function SignUpCTA() {
  const [formData, setFormData] = useState({ email: '', password: '' });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Sign up data:', formData);
  };

  return (
    <section className="bg-[#f8fafc] py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        {/* سمت چپ: توضیحات */}
        <div className="text-left">
          <div className="inline-block bg-[#dcfce7] text-[#16a34a] text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider mb-4">
            Start Your Journey
          </div>
          <h2 className="text-4xl sm:text-5xl font-extrabold text-[#0f172a] tracking-tight leading-tight mb-6">
            Transform Your Baseline Today
          </h2>
          <p className="text-slate-600 text-base leading-relaxed mb-8">
            Join the collective. Create your anatomical profile in less than 3 minutes, set your precise physical goals, and let our engine draft your first high-performance roadmap.
          </p>

          <ul className="space-y-4">
            {[
              '100% personalized macro calculations',
              'Expert designed workout loops & injury blocks',
              'Direct trainer check-ins available weekly',
            ].map((feature, idx) => (
              <li key={idx} className="flex items-center gap-3 text-slate-800 font-medium text-sm">
                <span className="flex items-center justify-center w-5 h-5 rounded-full bg-[#dcfce7] text-[#16a34a] text-xs font-bold">
                  ✓
                </span>
                {feature}
              </li>
            ))}
          </ul>
        </div>

        {/* سمت راست: فرم ثبت‌نام */}
        <div className="bg-white p-8 rounded-3xl shadow-sm border border-slate-100 max-w-md w-full mx-auto lg:ml-auto">
          <h3 className="text-2xl font-bold text-slate-900 mb-1">Create Your Account</h3>
          <p className="text-slate-500 text-xs mb-6">Start with a 14-day premium trial, no credit card required.</p>

          <form onSubmit={handleSubmit} className="space-y-4 text-left">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
              <input
                type="email"
                placeholder="alex@gmail.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-200 bg-slate-50/50 text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900 focus:bg-white transition-all"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
              <input
                type="password"
                placeholder="Choose a secure password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-200 bg-slate-50/50 text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900 focus:bg-white transition-all"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-[#0f172a] hover:bg-slate-800 text-white font-medium py-3 rounded-lg text-sm transition-colors mt-2"
            >
              Sign Up Now
            </button>
          </form>

          <p className="text-center text-xs text-slate-500 mt-6">
            Already have an account?{' '}
            <a href="#login" className="text-[#16a34a] font-semibold hover:underline">
              Log In
            </a>
          </p>
        </div>
      </div>
    </section>
  );
}
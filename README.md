# 🍏🏋️ Diet and Workout Plan API ( برنامه غذایی و ورزشی)

این پروژه، بخش بک‌اند (Backend) یک سیستم مدیریت و ارائه برنامه‌های غذایی و ورزشی است که با استفاده از فریم‌ورک **FastAPI** و زبان پایتون توسعه داده شده است. مدیریت دیتابیس در این پروژه بر عهده **SQLAlchemy** و **Alembic** می‌باشد.

## 🛠️ تکنولوژی‌های استفاده شده
- **فریم‌ورک:** FastAPI
- **دیتابیس:** PostgreSQL (از طریق async SQLAlchemy)
- **مایگریشن دیتابیس:** Alembic
- **زبان برنامه‌نویسی:** Python 3.x

## 📂 ساختار پروژه
پروژه با معماری لایه‌ای (Layered Architecture) طراحی شده است:
- `alembic/`: تنظیمات و فایل‌های مربوط به مایگریشن‌های دیتابیس.
- `app/`: کدهای اصلی برنامه.
  - `core/`: تنظیمات پایه، سکیوریتی و وابستگی‌های اصلی.
  - `models/`: مدل‌های دیتابیس (جداول SQLAlchemy).
  - `schemas/`: طرح‌های Pydantic برای اعتبارسنجی داده‌های ورودی و خروجی.
  - `repository/`: کلاس‌ها و توابع ارتباط مستقیم با دیتابیس (CRUD).
  - `services/`: منطق تجاری برنامه (Business Logic).
  - `routers/`: مسیرهای API (Endpoints).
- `requirements.txt`: لیست پکیج‌های مورد نیاز پروژه.
- `.env`: متغیرهای محیطی (شامل اطلاعات اتصال به دیتابیس و کلیدهای امنیتی).

## 🚀 راه‌اندازی پروژه در محیط محلی (Local)

### پیش‌نیازها
- نصب بودن Python 3.9 به بالا
- نصب و اجرای دیتابیس PostgreSQL

### ۱. نصب وابستگی‌ها
ابتدا یک محیط مجازی (Virtual Environment) بسازید و آن را فعال کنید:
```bash
python -m venv venv
# فعال‌سازی در ویندوز:
venv\Scripts\activate
# فعال‌سازی در مک/لینوکس:
source venv/bin/activate
سپس پکیج‌های مورد نیاز را نصب کنید:
bash
pip install -r requirements.txt

### ۲. تنظیم متغیرهای محیطی (.env)
یک فایل به نام `.env` در مسیر اصلی پروژه (در صورت عدم وجود) بسازید و اطلاعات مربوط به دیتابیس خود را در آن وارد کنید. مثال:
env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/db_name
SECRET_KEY=your_secret_key
*(توجه: فایل `.env` هرگز نباید در گیت کامیت شود)*

### ۳. اعمال مایگریشن‌های دیتابیس
برای ساخت جداول در دیتابیس، دستور زیر را اجرا کنید:
bash
alembic upgrade head

### ۴. ایجاد ادمین پیش‌فرض (اختیاری)
برای ساخت اولین کاربر ادمین جهت ورود به سیستم می‌توانید اسکریپت مربوطه را اجرا کنید:
bash
python app/create_admin.py

### ۵. اجرای سرور
برای اجرای برنامه از Uvicorn استفاده کنید:
bash
uvicorn app.main:app --reload
برنامه در آدرس `http://127.0.0.1:8000` اجرا خواهد شد.

## 📖 مستندات API
با توجه به ویژگی‌های جذاب FastAPI، مستندات تعاملی API به صورت خودکار تولید می‌شوند. پس از اجرای سرور می‌توانید به لینک‌های زیر مراجعه کنید:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`


**چند نکته:**
1. در بخش تنظیم فایل `.env`، فرمت `DATABASE_URL` را متناسب با نام متغیری که خودتان در فایل `app/config.py` یا `app/database.py` تعریف کرده‌اید تغییر دهید.
2. این فایل `README.md` را می‌توانید بعدا که گیت را روی سیستم نصب کردید، همراه با بقیه کدهایتان به گیت‌هاب پوش (Push) کنید تا صفحه اول مخزن شما ظاهر مرتب و حرفه‌ای داشته باشد.

# برنامه ورزشی و غذایی — فرانت‌اند

اسکلت اولیه‌ی پروژه با React + Vite، بر پایه‌ی معماری **feature-based** تا در آینده به‌راحتی قابل توسعه باشد.

## تکنولوژی‌ها
- **React 18** + **Vite** — سریع و سبک
- **React Router v6** — روتینگ + lazy loading صفحات
- **Redux Toolkit** — مدیریت state سراسری (هر feature یک slice مستقل)
- **Axios** — لایه‌ی ارتباط با API، با interceptor برای توکن و خطاها
- **React Hook Form** — فرم‌ها
- **Tailwind CSS** — استایل‌دهی سریع و یکدست

## ساختار پوشه‌ها

```
src/
├── app/                  # پیکربندی سراسری (redux store)
├── assets/               # عکس‌ها و آیکون‌ها
├── components/
│   ├── common/           # کامپوننت‌های عمومی UI (Button, Input, Card, Loader)
│   └── layout/            # Header, Sidebar, MainLayout
├── config/               # متغیرهای محیطی
├── features/             # هسته‌ی اصلی معماری — هر ماژول کاملاً مستقل
│   ├── auth/
│   │   ├── api/          # فراخوانی‌های API مخصوص این feature
│   │   ├── components/   # کامپوننت‌های UI مخصوص این feature
│   │   ├── hooks/        # هوک‌های مخصوص این feature
│   │   └── authSlice.js  # state management مخصوص این feature
│   ├── workouts/         # همین الگو
│   ├── nutrition/        # همین الگو
│   ├── dashboard/
│   └── profile/          # اسکلت آماده، فقط باید تکمیل شود
├── hooks/                # هوک‌های عمومی مشترک بین کل اپ
├── routes/               # تعریف مسیرها و route های محافظت‌شده
├── services/             # apiClient مشترک (axios instance)
├── styles/               # CSS سراسری
├── App.jsx
└── main.jsx
```

## چرا این ساختار؟

هر **feature** (auth، workouts، nutrition، ...) یک پوشه‌ی مستقل با api/components/hooks/slice خودش دارد.
این یعنی:
- برای افزودن قابلیت جدید (مثلاً «پیشرفت و آمار»)، کافیست یک پوشه‌ی جدید در `features/` بسازید — چیزی در جاهای دیگر پروژه نباید تغییر کند.
- کامپوننت‌های `components/common` و `components/layout` فقط UI عمومی هستند و به هیچ feature خاصی وابسته نیستند.
- تمام درخواست‌های HTTP از یک `apiClient` واحد در `services/` عبور می‌کنند (مدیریت توکن، خطای 401، و غیره در یک‌جا).

## افزودن یک feature جدید (مثال)

1. `src/features/progress/` بسازید با زیرپوشه‌های `api/`, `components/`, `hooks/`
2. `progressSlice.js` را طبق الگوی `workoutSlice.js` بنویسید
3. reducer را در `src/app/store.js` اضافه کنید
4. صفحه را به‌صورت lazy در `src/routes/AppRoutes.jsx` اضافه کنید

## راه‌اندازی

```bash
npm install
cp .env.example .env   # آدرس API بک‌اند را تنظیم کنید
npm run dev
```

## نکات باقی‌مانده برای شما
- فیچر `profile` فقط اسکلت پوشه دارد؛ طبق الگوی `workouts` تکمیلش کنید.
- فونت `Vazirmatn` باید جداگانه import یا از CDN اضافه شود (در `index.html` یا `globals.css`).
- در حال حاضر state ورودی/خروجی به‌صورت mock نیست — به بک‌اند واقعی روی `VITE_API_BASE_URL` وصل می‌شود.

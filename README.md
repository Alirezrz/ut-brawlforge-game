# 🎮 Python Multiplayer Game Project

Welcome to the project repository! 

For a complete overview of the game's features, networking architecture, please review our  presentation document:

👉 **[View the Project Presentation PDF](https://github.com/Alirezrz/ut-brawlforge-game/blob/main/Presentation.pdf)**



# UT Brawlforge

## ساختار پروژه

در زیر ساختار فایل‌ها و پوشه‌های اصلی پروژه به همراه توضیح مختصری از هرکدام آورده شده است:

```
.
├── config.py        # تنظیمات و پیکربندی‌های اصلی بازی (مانند ابعاد صفحه، سرعت و ...)
├── .git             # پوشه مربوط به سیستم کنترل نسخه گیت (نادیده گرفته شود)
├── .gitignore
├── README.md        
├── requirements.txt # لیست کتابخانه‌ها و وابستگی‌های لازم برای اجرای پروژه
├── run_game.py      # اسکریپت اصلی برای اجرای بازی
└── src              # پوشه اصلی کدهای منبع بازی
    ├── assets       # شامل فایل‌های جانبی بازی مانند تصاویر و صداها
    │   ├── images   # پوشه تصاویر استفاده شده در بازی
    │   │   └── .gitkeep   
    │   └── sounds   # پوشه صداهای استفاده شده در بازی
    │       └── .gitkeep
    ├── engine       # شامل منطق اصلی و موتور بازی
    │   ├── game.py  # کلاس‌ها و توابع اصلی مربوط به گیم‌پلی و مدیریت بازی
    │   └── __init__.py # فایل مورد نیاز پایتون برای شناسایی این پوشه به عنوان یک پکیج
    └── utils.py     # شامل توابع کمکی و ابزارهای عمومی مورد استفاده در پروژه
```

## نحوه نصب و اجرا

برای نصب و اجرای این پروژه، مراحل زیر را دنبال کنید:
**نصب dependencyها:**

    کتابخانه‌های مورد نیاز پروژه را با استفاده از فایل `requirements.txt` نصب کنید:
    ```bash
    pip install -r requirements.txt
    ```
یا اینکه فایل install_requirements را اجرا کنید. 

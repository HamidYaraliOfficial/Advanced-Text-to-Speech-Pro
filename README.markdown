# Advanced Text-to-Speech Pro

---

## English

### Overview
**Advanced Text-to-Speech Pro** is a feature-rich, modern desktop application built with **Python** and **PyQt6**, powered by **Google's gTTS** engine. It converts any input text into natural-sounding speech with support for **multiple languages**, **accents**, **speed/volume control**, and **custom themes**.

Perfect for accessibility tools, language learning, content creation, and automation — all wrapped in a sleek, animated, and fully translatable interface.

---

### Key Features
- **Real-time TTS Conversion** using Google’s high-quality voices
- **Multilingual Support**:
  - English, Persian (فارسی), Chinese (中文), Russian (Русский), and more
  - Full **RTL layout** support for Persian and Arabic-based languages
- **Accent Selection (TLD)**:
  - US, UK, Canada, Australia, India, Ireland, etc.
- **Audio Controls**:
  - Adjustable **speed** (0.5x to 2.0x)
  - Adjustable **volume** (0% to 100%)
  - **Play**, **Stop**, and **Save** functionality
- **Output Formats**:
  - MP3 (default)
  - WAV (coming soon)
- **Smart Chunking**:
  - Handles **very long texts** (up to 5000+ characters) by splitting safely
- **Threaded Processing**:
  - No UI freeze during conversion
  - Real-time **progress bar**
- **5 Stunning Themes**:
  - Windows 11 (Native)
  - Light
  - Dark
  - Ocean Blue
  - Crimson Red
- **Settings Persistence**:
  - Auto-save path
  - Default filename
  - Auto-save after conversion
- **Professional UI**:
  - Smooth animations
  - Gradient backgrounds
  - Custom icons
  - Tabbed interface

---

### Requirements
- Python 3.8+
- PyQt6
- gTTS
- pygame
- tempfile, uuid (standard library)

---

### Installation
1. Install dependencies:
   ```bash
   pip install PyQt6 gTTS pygame
   ```
2. Save the script as `tts_pro.py`
3. (Optional) Add icons: `icon.ico`, `convert.png`, `save.png`, `play.png`, `stop.png`
4. Run:
   ```bash
   python tts_pro.py
   ```

---

### Usage
1. **Enter or paste** your text in the input area.
2. Select **language** and **accent (TLD)**.
3. Adjust **speed** and **volume** as needed.
4. Click **"Convert to Speech"**.
5. Use **Play**, **Stop**, or **Save As...** to manage the audio.
6. Switch **themes** and **languages** instantly.

> Pro Tip: Enable **"Auto Save After Conversion"** in Settings for seamless workflow.

---

### Project Structure
- `tts_pro.py` – Full standalone application
- `icon.ico` – (Optional) Window icon
- `convert.png`, `save.png`, `play.png`, `stop.png` – (Optional) Button icons

---

### Contributing
We welcome contributions!  
You can:
- Add new languages
- Support more audio formats (WAV, OGG)
- Improve voice quality
- Add voice selection (male/female)
- Enhance animations

Submit a **Pull Request** with clear descriptions.

---

### License
Released under the **MIT License**. Free for personal and commercial use.

---

## فارسی

### نمای کلی
**استودیو پیشرفته تبدیل متن به گفتار** یک برنامه دسکتاپ حرفه‌ای و مدرن است که با **پایتون** و **PyQt6** ساخته شده و از موتور **gTTS گوگل** استفاده می‌کند. این ابزار هر متنی را به گفتار طبیعی با پشتیبانی از **زبان‌های مختلف**، **لهجه‌ها**، **کنترل سرعت و حجم صدا** و **تم‌های زیبا** تبدیل می‌کند.

مناسب برای ابزارهای دسترسی، یادگیری زبان، تولید محتوا و اتوماسیون — با رابطی شیک، انیمیشنی و کاملاً قابل ترجمه.

---

### ویژگی‌های کلیدی
- **تبدیل لحظه‌ای متن به گفتار** با صدای باکیفیت گوگل
- **پشتیبانی چندزبانه**:
  - فارسی، انگلیسی، چینی، روسی و ...
  - پشتیبانی کامل از **چیدمان راست‌به‌چپ (RTL)**
- **انتخاب لهجه (TLD)**:
  - آمریکا، بریتانیا، کانادا، استرالیا، هند، ایرلند و ...
- **کنترل‌های صوتی**:
  - تنظیم **سرعت** (۰.۵ تا ۲ برابر)
  - تنظیم **حجم صدا** (۰ تا ۱۰۰٪)
  - دکمه‌های **پخش**، **توقف** و **ذخیره**
- **فرمت‌های خروجی**:
  - MP3 (پیش‌فرض)
  - WAV (به‌زودی)
- **تقسیم هوشمند متن**:
  - مدیریت متن‌های **بسیار طولانی** (بیش از ۵۰۰۰ کاراکتر)
- **پردازش در ترد جدا**:
  - بدون قفل شدن رابط کاربری
  - نمایش **نوار پیشرفت** لحظه‌ای
- **۵ تم خیره‌کننده**:
  - ویندوز ۱۱ (بومی)
  - روشن
  - تاریک
  - آبی اقیانوسی
  - قرمز کریمسون
- **ذخیره تنظیمات**:
  - مسیر ذخیره خودکار
  - نام فایل پیش‌فرض
  - ذخیره خودکار پس از تبدیل
- **رابط حرفه‌ای**:
  - انیمیشن‌های نرم
  - پس‌زمینه گرادیان
  - آیکون‌های سفارشی
  - رابط تب‌دار

---

### پیش‌نیازها
- پایتون ۳.۸ یا بالاتر
- PyQt6
- gTTS
- pygame

---

### نصب
1. نصب کتابخانه‌ها:
   ```bash
   pip install PyQt6 gTTS pygame
   ```
2. فایل را با نام `tts_pro.py` ذخیره کنید
3. (اختیاری) آیکون‌ها را اضافه کنید: `icon.ico`, `convert.png`, `save.png`, `play.png`, `stop.png`
4. اجرا:
   ```bash
   python tts_pro.py
   ```

---

### نحوه استفاده
1. **متن خود را وارد یا پیست کنید**.
2. **زبان** و **لهجه** را انتخاب کنید.
3. **سرعت** و **حجم صدا** را تنظیم کنید.
4. روی **«تبدیل به گفتار»** کلیک کنید.
5. از دکمه‌های **پخش**، **توقف** یا **ذخیره با نام...** استفاده کنید.
6. **تم** و **زبان** را در لحظه تغییر دهید.

> نکته حرفه‌ای: در تنظیمات، گزینه **«ذخیره خودکار پس از تبدیل»** را فعال کنید.

---

### ساختار پروژه
- `tts_pro.py` – برنامه کامل و مستقل
- `icon.ico` – (اختیاری) آیکون پنجره
- `convert.png`, `save.png`, `play.png`, `stop.png` – (اختیاری) آیکون دکمه‌ها

---

### مشارکت
مشارکت شما بسیار ارزشمند است!  
می‌توانید:
- زبان‌های جدید اضافه کنید
- فرمت‌های صوتی بیشتری پشتیبانی کنید
- کیفیت صدا را بهبود دهید
- انتخاب صدا (مرد/زن) اضافه کنید
- انیمیشن‌ها را ارتقا دهید

درخواست کشش (Pull Request) با توضیحات واضح ارسال کنید.

---

### مجوز
تحت **مجوز MIT** منتشر شده است. آزاد برای استفاده شخصی و تجاری.

---

## 中文

### 项目概览
**高级文本转语音 Pro** 是一款功能丰富、界面现代的桌面应用程序，使用 **Python** 和 **PyQt6** 构建，基于 **Google gTTS** 引擎。它可以将任意输入文本转换为自然流畅的语音，支持 **多语言**、**口音选择**、**速度/音量控制** 以及 **精美主题**。

适用于无障碍工具、语言学习、内容创作和自动化 — 拥有流畅动画和完全可翻译的界面。

---

### 核心功能
- **实时文本转语音**，采用谷歌高品质语音
- **多语言支持**：
  - 中文、英语、波斯语、俄语等
  - 完整支持 **从右到左 (RTL)** 布局
- **口音选择 (TLD)**：
  - 美国、英国、加拿大、澳大利亚、印度、爱尔兰等
- **音频控制**：
  - 可调 **速度** (0.5x 至 2.0x)
  - 可调 **音量** (0% 至 100%)
  - **播放**、**停止**、**另存为**
- **输出格式**：
  - MP3（默认）
  - WAV（即将支持）
- **智能分块处理**：
  - 支持 **超长文本**（5000+ 字符）
- **线程化处理**：
  - 转换时不卡顿界面
  - 实时 **进度条**
- **5 种精美主题**：
  - Windows 11（原生）
  - 浅色
  - 深色
  - 海洋蓝
  - 绯红
- **设置持久化**：
  - 自动保存路径
  - 默认文件名
  - 转换后自动保存
- **专业界面**：
  - 平滑动画
  - 渐变背景
  - 自定义图标
  - 标签页导航

---

### 系统要求
- Python 3.8+
- PyQt6
- gTTS
- pygame

---

### 安装步骤
1. 安装依赖：
   ```bash
   pip install PyQt6 gTTS pygame
   ```
2. 将脚本保存为 `tts_pro.py`
3. （可选）添加图标：`icon.ico`、`convert.png`、`save.png`、`play.png`、`stop.png`
4. 运行：
   ```bash
   python tts_pro.py
   ```

---

### 使用指南
1. 在输入区 **输入或粘贴** 文本。
2. 选择 **语言** 和 **口音 (TLD)**。
3. 调整 **速度** 和 **音量**。
4. 点击 **“转换为语音”**。
5. 使用 **播放**、**停止** 或 **另存为** 管理音频。
6. 随时切换 **主题** 和 **语言**。

> 专业提示：在“设置”中启用 **“转换后自动保存”** 以提升效率。

---

### 项目结构
- `tts_pro.py` – 完整独立应用程序
- `icon.ico` – （可选）窗口图标
- `convert.png`, `save.png`, `play.png`, `stop.png` – （可选）按钮图标

---

### 贡献代码
我们非常欢迎贡献！您可以：
- 添加新语言
- 支持更多音频格式（WAV、OGG）
- 提升语音质量
- 增加音色选择（男声/女声）
- 优化动画效果

请提交带有清晰说明的 **Pull Request**。

---

### 许可证
基于 **MIT 许可证** 发布。个人和商业用途完全免费。
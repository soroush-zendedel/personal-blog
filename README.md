# Sabt-e Ahval (Personal Blog)

**Sabt-e Ahval** is Soroush Zendedel’s personal notebook for essays, reflections, poetry, and stories—a place to write at the intersection of technology and emotion.

- **Website:** [soroush-zendedel.github.io/personal-blog](https://soroush-zendedel.github.io/personal-blog/)
- **Author:** Soroush Zendedel — Technical Artist and Writer
- **Primary language:** Persian. Individual English posts can also be marked in their metadata.

## Content

Posts are organized by topic under `docs/posts/`:

| Directory | Content |
| --- | --- |
| `poetry/` | Poems, with subcategories such as `ravi/`, `khiyal/`, and `nostalgia/` |
| `journal/` | Personal narratives and ongoing series |
| `reflections/` | Notes and reflections |
| `short-stories/` | Short stories |
| `geek/` | Technology and geek-related writing |

The homepage in `docs/index.md` displays posts marked `main_page: true`. `docs/tags.md` provides the tag index. Images and other static assets live in `docs/assets/`.

## Run locally

The site is built with Python and MkDocs. You need Python 3 and `pip`. From the repository root, create a virtual environment:

```bash
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies and start the local preview:

```bash
python -m pip install -r requirements.txt
mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The preview refreshes when files change. To build the static site into the ignored `site/` directory, run:

```bash
mkdocs build
```

### Docker Compose

Install Docker Desktop or Docker Engine with Compose v2. Start the live development preview from the repository root:

```bash
docker compose --profile dev up --build
```

Open [http://localhost:8000](http://localhost:8000). The repository is mounted into the container, so changes to Markdown, images, styles, and configuration appear in the live preview. Stop it with `Ctrl+C`, or run `docker compose --profile dev down` in another terminal. To use a different host port, set `MKDOCS_PORT` (for example, `$env:MKDOCS_PORT=8001` in PowerShell, then run the command again).

To build and run the optimized static site with Nginx instead, use the production profile:

```bash
docker compose --profile production up --build
```

Open [http://localhost:8080](http://localhost:8080). Rebuild with `--build` after changing site content. Stop it with `Ctrl+C` or `docker compose --profile production down`. Set `BLOG_PORT` to choose a different host port.

If the default PyPI file host is unreachable during the image build, use the Tsinghua PyPI mirror variant:

```bash
docker compose --profile dev-mirror up --build
```

This uses `Dockerfile.mirror`, which installs Debian and Python packages from Tsinghua mirrors, and serves the live preview at [http://localhost:8002/personal-blog/](http://localhost:8002/personal-blog/). The host port can be changed with `MKDOCS_MIRROR_PORT`. Stop it with `Ctrl+C` or `docker compose --profile dev-mirror down`. The mirrors must be reachable from Docker; see the [Tsinghua Debian mirror instructions](https://mirrors.tuna.tsinghua.edu.cn/help/debian/) and [PyPI mirror instructions](https://mirror.tuna.tsinghua.edu.cn/help/pypi/).

## Add or edit a post

Create a Markdown file with YAML metadata at the top. For example:

```markdown
---
title: "Post title"
description: "A short description for the page and search engines."
category: "Essay"
date: "2026-10-19"
excerpt: "A short summary shown on the post card."
image: assets/images/example/cover.jpg
image_alt: "A text description of the image for accessibility."
image_caption: "Optional image caption."
tags:
  - reflection
  - ideas
main_page: true
---

# Post title

Write the post here.
```

Existing posts use `title`, `description`, `category`, `date`, `excerpt`, and `tags`. The image and its alt text are optional. If `image_caption` is omitted, the theme uses `excerpt` as the caption. Set `main_page: true` to include a post in the homepage cards; posts without it remain accessible through their category pages and search. Set `draft: true` to omit a post from the homepage cards. For English content, set `english: true` to enable left-to-right layout.

Keep the file path aligned with its category—for example, `docs/posts/poetry/ravi/new-poem.md`. Put images in an appropriate subdirectory of `docs/assets/images/` and use a path relative to `docs/` in the metadata.

## Deployment

The repository is configured to publish automatically to GitHub Pages. Every push to `main` triggers [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which installs the dependencies and runs `mkdocs gh-deploy --force`. The generated site is published to the `gh-pages` branch. For deployment to work, configure GitHub Pages to serve from `gh-pages` and allow the workflow to write repository contents.

## Project structure

```text
.
├── .github/workflows/deploy.yml  # Automated build and deployment
├── Dockerfile                    # Development and production image targets
├── Dockerfile.mirror             # Development image using the Tsinghua PyPI mirror
├── compose.yaml                  # Local development and static site services
├── .dockerignore                 # Files excluded from Docker build context
├── docs/                         # Website pages and content
│   ├── assets/                   # Images, fonts, CSS, and JavaScript
│   ├── posts/                    # Essays, poems, and stories
│   ├── index.md                  # Homepage
│   └── tags.md                   # Tag index
├── overrides/                    # Custom theme templates
├── main.py                       # MkDocs macros for post cards
├── mkdocs.yml                    # Site and plugin configuration
└── requirements.txt              # Python dependencies
```

## Technology

- [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- MkDocs plugins for search, tags, image galleries, Git revision dates, and page generation
- Custom Python macros for rendering post cards on the homepage
- GitHub Actions and GitHub Pages for deployment

---

# ثبت‌احوال

**ثبت‌احوال** دفتر نوشته‌ها، درددل‌ها، شعرها و روایت‌های سروش زنده‌دل است؛ جایی برای ثبت تجربه‌ها در تقاطع تکنولوژی و احساس.

- **وب‌سایت:** [soroush-zendedel.github.io/personal-blog](https://soroush-zendedel.github.io/personal-blog/)
- **نویسنده:** سروش زنده‌دل — تکنیکال آرتیست و نویسنده
- **زبان اصلی:** فارسی؛ امکان مشخص‌کردن نوشته‌های انگلیسی نیز در فراداده وجود دارد.

## محتوا

مطالب در `docs/posts/` و بر اساس موضوع دسته‌بندی شده‌اند:

| پوشه | نوع محتوا |
| --- | --- |
| `poetry/` | شعرها، با زیردسته‌هایی مانند `ravi/`، `khiyal/` و `nostalgia/` |
| `journal/` | روایت‌ها و نوشته‌های دنباله‌دار |
| `reflections/` | یادداشت‌ها و تأمل‌ها |
| `short-stories/` | داستان‌های کوتاه |
| `geek/` | نوشته‌های مرتبط با تکنولوژی و موضوعات گیک |

صفحهٔ اصلی در `docs/index.md` نوشته‌های دارای `main_page: true` را نمایش می‌دهد. صفحهٔ `docs/tags.md` نمایهٔ برچسب‌ها را ارائه می‌کند. تصویرها و سایر فایل‌های ثابت در `docs/assets/` نگهداری می‌شوند.

## اجرا و پیش‌نمایش محلی

پروژه با Python و MkDocs ساخته شده است. Python 3 و `pip` لازم است. در PowerShell یا ترمینال، از ریشهٔ مخزن اجرا کنید:

```bash
python -m venv .venv
```

فعال‌سازی محیط مجازی در PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

در macOS یا Linux:

```bash
source .venv/bin/activate
```

سپس وابستگی‌ها را نصب و پیش‌نمایش محلی را اجرا کنید:

```bash
python -m pip install -r requirements.txt
mkdocs serve
```

پیش‌نمایش در [http://127.0.0.1:8000](http://127.0.0.1:8000) در دسترس خواهد بود و با ذخیرهٔ تغییرات به‌روز می‌شود. برای ساخت نسخهٔ ایستای سایت در پوشهٔ نادیده‌گرفته‌شدهٔ `site/` اجرا کنید:

```bash
mkdocs build
```

### داکر کامپوز

Docker Desktop یا Docker Engine به‌همراه Compose نسخهٔ ۲ را نصب کنید. برای اجرای پیش‌نمایش توسعه از ریشهٔ مخزن بزنید:

```bash
docker compose --profile dev up --build
```

سپس [http://localhost:8000](http://localhost:8000) را باز کنید. پوشهٔ پروژه داخل کانتینر mount می‌شود؛ تغییر فایل‌های Markdown، تصویرها، استایل‌ها و تنظیمات در پیش‌نمایش زنده دیده می‌شود. برای توقف `Ctrl+C` را بزنید یا در ترمینال دیگری `docker compose --profile dev down` را اجرا کنید. برای انتخاب پورت دیگری روی میزبان، مقدار `MKDOCS_PORT` را تنظیم کنید؛ مثلاً در PowerShell ابتدا `$env:MKDOCS_PORT=8001` و سپس دستور اجرا را وارد کنید.

برای ساخت و اجرای نسخهٔ ایستای بهینه‌شده با Nginx از پروفایل production استفاده کنید:

```bash
docker compose --profile production up --build
```

سایت در [http://localhost:8080](http://localhost:8080) در دسترس است. پس از تغییر محتوا، با `--build` دوباره image را بسازید. برای توقف `Ctrl+C` یا `docker compose --profile production down` را اجرا کنید. با تنظیم `BLOG_PORT` می‌توانید پورت میزبان را تغییر دهید.

اگر هنگام ساخت image دسترسی به میزبان فایل‌های PyPI برقرار نیست، نسخهٔ آینهٔ Tsinghua را اجرا کنید:

```bash
docker compose --profile dev-mirror up --build
```

این روش از `Dockerfile.mirror` استفاده می‌کند؛ بسته‌های Debian و Python را از آینه‌های Tsinghua دریافت می‌کند و پیش‌نمایش زنده را در [http://localhost:8002/personal-blog/](http://localhost:8002/personal-blog/) اجرا می‌کند. پورت میزبان را با `MKDOCS_MIRROR_PORT` می‌توانید تغییر دهید. برای توقف `Ctrl+C` یا `docker compose --profile dev-mirror down` را اجرا کنید. آینه‌ها باید از داخل Docker در دسترس باشند؛ راهنمای [آینهٔ Debian](https://mirrors.tuna.tsinghua.edu.cn/help/debian/) و [آینهٔ PyPI](https://mirror.tuna.tsinghua.edu.cn/help/pypi/) را ببینید.

## افزودن یا ویرایش نوشته

یک فایل Markdown با فرادادهٔ YAML در ابتدای آن بسازید. برای نمونه:

```markdown
---
title: "عنوان نوشته"
description: "توضیح کوتاه برای صفحه و موتورهای جستجو."
category: "نوشته"
date: "۱۴۰۵/۰۷/۲۷"
excerpt: "چکیده‌ای که در کارت نوشته نمایش داده می‌شود."
image: assets/images/example/cover.jpg
image_alt: "توضیح متنی تصویر برای دسترس‌پذیری."
image_caption: "زیرنویس تصویر؛ اختیاری."
tags:
  - دل‌نوشته
  - تأمل
main_page: true
---

# عنوان نوشته

متن نوشته را اینجا بنویسید.
```

فیلدهای `title`، `description`، `category`، `date`، `excerpt` و `tags` در نمونه‌های موجود استفاده می‌شوند. تصویر و متن جایگزین آن اختیاری‌اند. اگر `image_caption` مشخص نشود، قالب از `excerpt` به‌عنوان زیرنویس تصویر استفاده می‌کند. `main_page: true` نوشته را در کارت‌های صفحهٔ اصلی قرار می‌دهد؛ بدون این مقدار، نوشته همچنان از مسیر دسته‌بندی و جستجو قابل دسترسی است. برای پنهان‌کردن پیش‌نویس از کارت‌های صفحهٔ اصلی، `draft: true` بگذارید. برای محتوای انگلیسی `english: true` جهت و چیدمان چپ‌به‌راست را فعال می‌کند.

مسیر پیشنهادی فایل با دسته‌بندی هماهنگ باشد؛ برای مثال `docs/posts/poetry/ravi/new-poem.md`. فایل تصویر را در زیرپوشه‌ای مناسب از `docs/assets/images/` قرار دهید و مسیر آن را نسبت به پوشهٔ `docs/` در فراداده بنویسید.

## انتشار

مخزن برای انتشار خودکار روی GitHub Pages تنظیم شده است. هر بار که به شاخهٔ `main` پوش می‌شود، گردش‌کار [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) وابستگی‌ها را نصب می‌کند و دستور `mkdocs gh-deploy --force` را اجرا می‌کند. خروجی در شاخهٔ `gh-pages` منتشر می‌شود. برای کارکرد انتشار، تنظیم GitHub Pages مخزن باید از شاخهٔ `gh-pages` سرویس بدهد و دسترسی نوشتن گردش‌کار به محتوا فعال باشد.

## ساختار پروژه

```text
.
├── .github/workflows/deploy.yml  # ساخت و انتشار خودکار
├── Dockerfile                    # imageهای توسعه و انتشار
├── Dockerfile.mirror             # image توسعه با آینهٔ Tsinghua برای PyPI
├── compose.yaml                  # سرویس‌های توسعه و سایت ایستا
├── .dockerignore                 # فایل‌های خارج از بافت ساخت Docker
├── docs/                         # صفحه‌ها و محتوای وب‌سایت
│   ├── assets/                   # تصویرها، فونت‌ها، CSS و JavaScript
│   ├── posts/                    # نوشته‌ها و شعرها
│   ├── index.md                  # صفحهٔ اصلی
│   └── tags.md                   # نمایهٔ برچسب‌ها
├── overrides/                    # قالب‌های سفارشی پوسته
├── main.py                       # ماکروهای MkDocs برای کارت نوشته‌ها
├── mkdocs.yml                    # تنظیمات سایت و افزونه‌ها
└── requirements.txt              # وابستگی‌های Python
```

## فناوری‌ها

- [MkDocs](https://www.mkdocs.org/) و [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- افزونه‌های MkDocs برای جستجو، برچسب‌ها، گالری تصویر، تاریخچهٔ Git و ساخت صفحات
- ماکروهای سفارشی Python برای نمایش کارت‌های نوشته در صفحهٔ اصلی
- GitHub Actions و GitHub Pages برای انتشار

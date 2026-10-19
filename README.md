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

### Collection pages and navigation

Collection landing pages are generated during the MkDocs build by [`hooks/collections.py`](hooks/collections.py). The hook discovers every `.collection.yml` under `docs/posts/` and adds a virtual `index.md` for that directory; do not create or commit a manual `index.md` for a collection. The generated page is included in navigation, canonical metadata, and the project sitemap like other MkDocs pages.

To add a poetry book, journal, or other collection:

1. Create a directory beneath `docs/posts/` and add a `.collection.yml` file. Define a reader-facing `title`; `description` and `english: true` are optional.
2. Put each entry in its own Markdown file in that directory (or a nested directory). Add the usual post metadata, including `title` and `category`; the category becomes the visible section heading on the collection page. Entries marked `draft: true` are omitted.
3. Use a numeric `order` value in post metadata to set an explicit order within its category. If omitted, a leading number in the filename is used (for example, `00-pishgoftar.md`); entries without either sort after numbered entries.
4. Preview with `mkdocs serve` and verify the generated collection URL under the configured `site_url`.

Example `docs/posts/journal/my-series/.collection.yml`:

```yaml
title: My series
description: A short introduction to this collection.
```

The collection page, visible breadcrumb, and `BreadcrumbList` JSON-LD use the same collection metadata. Breadcrumbs include the main site root (`https://soroush-zendedel.github.io/`), the blog homepage, any containing collections from outermost to innermost, and the current page. The collection page does not link to itself as a parent. The main homepage has no breadcrumb.

The `.pages` files are separate Awesome Pages navigation settings, not content pages: they control sidebar labels, icons, and ordering. They remain intentionally explicit so the menu can use short Persian labels and custom icons. When adding a collection, add its directory name to the parent `.pages` `arrange` list if you need a specific menu position; add a child `.pages` file only when it needs a custom sidebar label or icon. These settings do not control generated page content, breadcrumbs, canonical URLs, or sitemap entries.

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

Keep the file path aligned with its category—for example, `docs/posts/poetry/ravi/new-poem.md`. Use a descriptive lowercase filename with hyphens between words (for example, `i-call-your-name.md`); keep the reader-facing title in the `title` metadata. MkDocs generates the sitemap from the current file paths, so do not edit `sitemap.xml` by hand. Put images in an appropriate subdirectory of `docs/assets/images/` and use a path relative to `docs/` in the metadata.

## Deployment

The repository is configured to publish automatically to GitHub Pages. Every push to `main` triggers [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which installs the dependencies and runs `mkdocs gh-deploy --force`. The generated site is published to the `gh-pages` branch. For deployment to work, configure GitHub Pages to serve from `gh-pages` and allow the workflow to write repository contents. The host-level `robots.txt` and sitemap index are maintained by the root-site repository; that index already includes this project's generated sitemap, so this subproject does not need its own `robots.txt`.

### SEO and structured data

The production base URL is `https://soroush-zendedel.github.io/personal-blog/`, a project site beneath the main site at `https://soroush-zendedel.github.io/`. MkDocs Material emits an absolute, self-referencing canonical URL for each page from `site_url`; keep this setting aligned with the published path. The built-in sitemap plugin writes this project's sitemap into the generated site, while the domain-level robots file and sitemap index remain managed by the root-site repository. Do not add `hreflang` links unless matching translated pages are available; English posts currently have no corresponding Persian/English page pairs.

The shared page template displays a breadcrumb after the article content and before the footer on non-home pages. The local MkDocs hook at `hooks/collections.py` reads `.collection.yml` files under `docs/posts/` and generates virtual collection index pages during build. The same collection metadata feeds the visible breadcrumb and Google-supported `BreadcrumbList` JSON-LD. Collection pages group posts by `category`; `order` or a numeric filename prefix controls their order. See [Collection pages and navigation](#collection-pages-and-navigation) for the add-a-collection instructions. The breadcrumb hierarchy is the main site, this blog's homepage, any containing collection pages from outermost to innermost, and the current page. `.pages` files separately control sidebar labels, icons, and ordering. The homepage has no breadcrumb. Pages marked `english: true` receive `lang="en"`; other pages use Persian (`fa`). No Article, ProfilePage, or SoftwareApplication markup is generated.

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
│   │   └── …/.collection.yml     # Collection metadata for generated index pages
│   ├── index.md                  # Homepage
│   └── tags.md                   # Tag index
├── hooks/collections.py          # Generated collection pages and shared metadata
├── overrides/                    # Custom theme templates
├── main.py                       # MkDocs macros for post cards
├── mkdocs.yml                    # Site and plugin configuration
└── requirements.txt              # Python dependencies
```

## Technology

- [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- MkDocs plugins for search, tags, image galleries, and Git revision dates; a local hook generates collection pages
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

<a id="collection-pages-and-navigation-fa"></a>

### صفحه‌های مجموعه و راهبری

صفحه‌های نمایهٔ مجموعه هنگام build توسط [`hooks/collections.py`](hooks/collections.py) ساخته می‌شوند. این hook همهٔ فایل‌های `.collection.yml` در `docs/posts/` را پیدا می‌کند و برای هر پوشه یک `index.md` مجازی به MkDocs می‌دهد؛ برای مجموعه‌ها `index.md` دستی نسازید یا commit نکنید. صفحهٔ تولیدشده مانند سایر صفحه‌های MkDocs وارد منو، canonical و sitemap پروژه می‌شود.

برای افزودن دفتر شعر، دفتر خاطرات یا مجموعه‌ای دیگر:

1. زیر `docs/posts/` پوشه بسازید و در آن `.collection.yml` بگذارید. `title` عنوان نمایشی مجموعه است؛ `description` و `english: true` اختیاری‌اند.
2. هر نوشته را در یک فایل Markdown داخل همان پوشه یا زیرپوشه‌اش قرار دهید. فرادادهٔ معمول نوشته، از جمله `title` و `category` را وارد کنید؛ مقدار `category` عنوان بخش قابل‌مشاهده در صفحهٔ مجموعه می‌شود. نوشته‌های دارای `draft: true` نمایش داده نمی‌شوند.
3. برای ترتیب صریح نوشته‌ها در هر دسته، در فراداده `order` عددی بگذارید. اگر این مقدار نباشد، عدد ابتدای نام فایل استفاده می‌شود؛ مثلاً `00-pishgoftar.md`. فایل‌های بدون `order` و پیشوند عددی پس از موارد شماره‌دار می‌آیند.
4. با `mkdocs serve` پیش‌نمایش بگیرید و نشانی صفحهٔ تولیدشده را زیر `site_url` تنظیم‌شده بررسی کنید.

نمونهٔ `docs/posts/journal/my-series/.collection.yml`:

```yaml
title: مجموعهٔ من
description: توضیح کوتاه این مجموعه.
```

صفحهٔ مجموعه، breadcrumb نمایان و JSON-LD از نوع `BreadcrumbList` از همان فرادادهٔ مجموعه استفاده می‌کنند. مسیر breadcrumb از ریشهٔ سایت اصلی (`https://soroush-zendedel.github.io/`)، خانهٔ وبلاگ، مجموعه‌های والد از بیرونی‌ترین تا درونی‌ترین و صفحهٔ جاری تشکیل می‌شود. صفحهٔ مجموعه به‌عنوان والد خودش تکرار نمی‌شود و صفحهٔ اصلی breadcrumb ندارد.

فایل‌های `.pages` تنظیمات جداگانهٔ افزونهٔ Awesome Pages برای منوی کناری‌اند، نه صفحهٔ محتوا؛ این فایل‌ها عنوان کوتاه منو، آیکن و ترتیب را کنترل می‌کنند. آن‌ها عمداً صریح مانده‌اند تا منو از عنوان‌های کوتاه فارسی و آیکن‌های سفارشی استفاده کند. هنگام افزودن مجموعه، اگر جای مشخصی در منو می‌خواهید نام پوشه را به فهرست `arrange` در `.pages` والد اضافه کنید؛ فقط اگر عنوان منو یا آیکن سفارشی لازم است برای مجموعه `.pages` فرزند بسازید. این تنظیمات محتوای صفحهٔ تولیدشده، breadcrumb، canonical یا sitemap را کنترل نمی‌کنند.

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

مسیر فایل با دسته‌بندی هماهنگ باشد؛ برای مثال `docs/posts/poetry/ravi/new-poem.md`. برای نام فایل از حروف کوچک و واژه‌های جداشده با خط تیره استفاده کنید؛ عنوان نمایشی خواننده را در فرادادهٔ `title` بنویسید. MkDocs سایتمپ را از مسیرهای فعلی فایل‌ها می‌سازد؛ بنابراین `sitemap.xml` را دستی ویرایش نکنید. فایل تصویر را در زیرپوشه‌ای مناسب از `docs/assets/images/` قرار دهید و مسیر آن را نسبت به پوشهٔ `docs/` در فراداده بنویسید.

## انتشار

مخزن برای انتشار خودکار روی GitHub Pages تنظیم شده است. هر بار که به شاخهٔ `main` پوش می‌شود، گردش‌کار [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) وابستگی‌ها را نصب می‌کند و دستور `mkdocs gh-deploy --force` را اجرا می‌کند. خروجی در شاخهٔ `gh-pages` منتشر می‌شود. برای کارکرد انتشار، تنظیم GitHub Pages مخزن باید از شاخهٔ `gh-pages` سرویس بدهد و دسترسی نوشتن گردش‌کار به محتوا فعال باشد. فایل `robots.txt` در ریشهٔ دامنه و نمایهٔ سایتمپ در مخزن سایت اصلی نگهداری می‌شوند؛ آن نمایه از قبل سایتمپ ساخته‌شدهٔ این پروژه را در بر می‌گیرد، پس این زیرپروژه به `robots.txt` جداگانه نیاز ندارد.

### سئو و داده‌های ساخت‌یافته

مسیر پایهٔ انتشار `https://soroush-zendedel.github.io/personal-blog/` و زیرمجموعهٔ سایت اصلی `https://soroush-zendedel.github.io/` است. Material برای MkDocs با توجه به `site_url` برای هر صفحه canonical مطلق و خودارجاع تولید می‌کند؛ این مقدار را با مسیر واقعی انتشار هماهنگ نگه دارید. افزونهٔ داخلی MkDocs سایتمپ این پروژه را در خروجی می‌سازد، اما فایل robots دامنه و نمایهٔ سایتمپ در مخزن سایت اصلی مدیریت می‌شوند. تا زمانی که صفحه‌های ترجمه‌شدهٔ معادل وجود ندارند، `hreflang` اضافه نکنید؛ نوشته‌های انگلیسی فعلی جفت معادل فارسی/انگلیسی ندارند.

قالب مشترک در صفحه‌های غیر از خانه، پس از محتوای نوشته و پیش از فوتر مسیر راهنما را نشان می‌دهد. hook محلی `hooks/collections.py` فایل‌های `.collection.yml` در `docs/posts/` را می‌خواند و صفحه‌های نمایهٔ مجازی را هنگام build می‌سازد. breadcrumb نمایان و JSON-LD از نوع `BreadcrumbList` از همان فرادادهٔ مجموعه استفاده می‌کنند. نوشته‌ها بر اساس `category` گروه‌بندی می‌شوند و `order` یا پیشوند عددی نام فایل ترتیب آن‌ها را تعیین می‌کند. راهنمای افزودن مجموعه در بخش [صفحه‌های مجموعه و راهبری](#collection-pages-and-navigation-fa) آمده است. سلسله‌مراتب breadcrumb سایت اصلی، خانهٔ وبلاگ، مجموعه‌های والد از بیرونی‌ترین تا درونی‌ترین و صفحهٔ جاری است. فایل‌های `.pages` جداگانه عنوان، آیکن و ترتیب منوی کناری را کنترل می‌کنند. خانه breadcrumb ندارد. زبان سند برای صفحه‌های دارای `english: true` برابر `en` است و برای بقیه `fa` می‌ماند. دادهٔ Article، ProfilePage یا SoftwareApplication تولید نمی‌شود.

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
│   │   └── …/.collection.yml     # فرادادهٔ مجموعه برای ساخت صفحهٔ نمایه
│   ├── index.md                  # صفحهٔ اصلی
│   └── tags.md                   # نمایهٔ برچسب‌ها
├── hooks/collections.py          # ساخت صفحه‌های مجموعه و فرادادهٔ مشترک
├── overrides/                    # قالب‌های سفارشی پوسته
├── main.py                       # ماکروهای MkDocs برای کارت نوشته‌ها
├── mkdocs.yml                    # تنظیمات سایت و افزونه‌ها
└── requirements.txt              # وابستگی‌های Python
```

## فناوری‌ها

- [MkDocs](https://www.mkdocs.org/) و [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- افزونه‌های MkDocs برای جستجو، برچسب‌ها، گالری تصویر و تاریخچهٔ Git؛ hook محلی برای ساخت صفحه‌های مجموعه
- ماکروهای سفارشی Python برای نمایش کارت‌های نوشته در صفحهٔ اصلی
- GitHub Actions و GitHub Pages برای انتشار

import os
import re
import html
import yaml

def extract_metadata(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        try:
            # استفاده از پارسر استاندارد برای خواندن صحیح لیست‌ها (مثل تگ‌ها)
            return yaml.safe_load(yaml_text) or {}
        except yaml.YAMLError:
            pass
    return {}

def define_env(env):
    @env.macro
    # پارامتر only_main_page را با مقدار پیش‌فرض False اضافه کردیم
    def get_recent_posts(base_folder="posts", limit=6, only_main_page=False):
        docs_dir = env.conf['docs_dir']
        target_dir = os.path.join(docs_dir, base_folder)
        
        if not os.path.exists(target_dir):
            return f"<p style='color:var(--crimson);'>پوشه {base_folder} یافت نشد.</p>"

        posts = []
        current_page_dir = os.path.dirname(env.page.file.src_uri)
        for root, dirs, files in os.walk(target_dir):
            for filename in files:
                if filename.endswith('.md') and filename != 'index.md':
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    metadata = extract_metadata(content)
                    
                    # در اینجا بررسی می‌کنیم که پست پیش‌نویس نباشد
                    if metadata and not metadata.get('draft', False):
                        
                        # بررسی شرط جدید: اگر درخواست شده فقط پست‌های صفحه اصلی نمایش داده شوند و این پست تگ main_page: true را نداشت، از آن عبور کن
                        if only_main_page and not metadata.get('main_page', False):
                            continue
                            
                        rel_dir = os.path.relpath(root, docs_dir).replace('\\', '/')
                        target_post_dir = os.path.join(rel_dir, os.path.splitext(filename)[0])
                        url_path = os.path.relpath(
                            target_post_dir, current_page_dir or '.'
                        ).replace('\\', '/') + '/'
                        
                        posts.append({
                            'title': metadata.get('title', 'بدون عنوان'),
                            'category': metadata.get('category', 'عمومی'),
                            'folder_name': os.path.basename(root), # <-- این خط نام پوشه را استخراج می‌کند
                            'date': metadata.get('date', 'بدون تاریخ'),
                            'excerpt': metadata.get('excerpt', '...'),
                            'image': metadata.get('image', ''), 
                            'tags': metadata.get('tags', []),
                            'url': url_path,
                            # --- بخش جدید: دریافت وضعیت زبان انگلیسی از متادیتا ---
                            'english': metadata.get('english', False) 
                            # --------------------------------------------------------
                        })
        
        posts.sort(key=lambda x: x['date'], reverse=True)
        
        html = '<div class="post-grid">\n'
        for post in posts[:limit]:
            img_src = post['image'] if post['image'] else 'assets/images/default-cover.svg'
            webp_path = os.path.splitext(img_src)[0] + '.webp'
            current_page_dir = os.path.dirname(env.page.file.src_uri)
            img_url = os.path.relpath(img_src, current_page_dir or '.').replace('\\', '/')
            webp_url = os.path.relpath(webp_path, current_page_dir or '.').replace('\\', '/')
            webp_src = (
                f'<source srcset="{webp_url}" type="image/webp">'
                if os.path.isfile(os.path.join(docs_dir, webp_path.replace('/', os.sep)))
                else ''
            )
            img_markup = (
                f'<picture>{webp_src}<img src="{img_url}" alt="{post["title"]}" class="post-card-cover skip-lightbox" loading="lazy" decoding="async" width="1600" height="900"></picture>'
                if webp_src
                else f'<img src="{img_url}" alt="{post["title"]}" class="post-card-cover skip-lightbox" loading="lazy" decoding="async" width="1600" height="900">'
            )
            
            tags_html = ''
            if post['tags']:
                tags_html = '<div class="post-card-tags">'
                for tag in post['tags'][:3]: 
                    tags_html += f'<span class="post-card-tag">#{tag}</span>'
                tags_html += '</div>'

            # --- بخش جدید: اعمال کلاس و دایرکشن در صورت انگلیسی بودن محتوا ---
            english_class = ' english-mode' if post['english'] else ''
            english_dir = ' dir="ltr"' if post['english'] else ''
            # -------------------------------------------------------------------

            # در این ساختار، متغیرهای جدید به تگ post-card افزوده می‌شوند
            html += f"""
            <div class="post-card{english_class}"{english_dir}>
                <a href="{post['url']}" class="post-card-image">
                    {img_markup}
                </a>
                <div class="post-card-content">
                    <span class="post-category">{post['category']}</span>
                    <h3><a href="{post['url']}" class="card-full-link">{post['title']}</a></h3>
                    <p class="post-excerpt">{post['excerpt']}</p>
                    {tags_html} <!-- تگ‌ها اینجا قرار می‌گیرند -->
                    <div class="post-meta">
                        <span>{post['date']}</span>
                        <span>{post['folder_name']}</span>
                    </div>
                </div>
            </div>
            """
        html += '</div>\n'
        
        return html

    @env.macro
    def collection_posts(collection_path):
        """Render a collection's posts grouped by their actual category metadata."""
        docs_dir = env.conf['docs_dir']
        target_dir = os.path.join(docs_dir, *collection_path.split('/'))
        current_dir = os.path.dirname(env.page.file.src_uri)
        groups = {}
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [name for name in dirs if not name.startswith('.')]
            for filename in files:
                if not filename.endswith('.md') or filename.lower() in {'index.md', 'readme.md'}:
                    continue
                source = os.path.join(root, filename)
                with open(source, 'r', encoding='utf-8') as file:
                    metadata = extract_metadata(file.read())
                if metadata.get('draft', False):
                    continue
                rel_dir = os.path.relpath(root, docs_dir).replace('\\', '/')
                destination = os.path.join(rel_dir, os.path.splitext(filename)[0])
                url = os.path.relpath(destination, current_dir or '.').replace('\\', '/') + '/'
                image = metadata.get('image', '')
                image_url = os.path.relpath(image, current_dir or '.').replace('\\', '/') if image else ''
                category = str(metadata.get('category', 'عمومی'))
                order = metadata.get('order')
                if order is None:
                    number = re.match(r'^\d+', filename)
                    order = int(number.group()) if number else 1_000_000
                try:
                    order = float(order)
                except (TypeError, ValueError):
                    order = 1_000_000
                groups.setdefault(category, []).append({
                    'title': str(metadata.get('title', os.path.splitext(filename)[0])),
                    'excerpt': str(metadata.get('excerpt', '')),
                    'date': str(metadata.get('date', '')),
                    'url': url,
                    'image': image_url,
                    'order': order,
                })

        if not groups:
            return '<p class="collection-empty">مطالب این دفتر هنوز منتشر نشده‌اند.</p>'

        output = []
        for category, posts in sorted(groups.items()):
            posts.sort(key=lambda post: (post['order'], post['title']))
            output.append(f'<section class="collection-topic"><h2>{html.escape(category)}</h2><div class="post-grid">')
            for post in posts:
                image = (f'<a href="{html.escape(post["url"], quote=True)}" class="post-card-image">'
                         f'<img src="{html.escape(post["image"], quote=True)}" alt="{html.escape(post["title"], quote=True)}" '
                         'class="post-card-cover skip-lightbox" loading="lazy" decoding="async" width="1600" height="900"></a>') if post['image'] else ''
                excerpt = f'<p class="post-excerpt">{html.escape(post["excerpt"])}</p>' if post['excerpt'] else ''
                date = f'<span>{html.escape(post["date"])}</span>' if post['date'] else ''
                output.append(
                    f'<article class="post-card">{image}<div class="post-card-content">'
                    f'<span class="post-category">{html.escape(category)}</span>'
                    f'<h3><a href="{html.escape(post["url"], quote=True)}">{html.escape(post["title"])}</a></h3>'
                    f'{excerpt}<div class="post-meta">{date}</div></div></article>'
                )
            output.append('</div></section>')
        return '\n'.join(output)


def on_post_build(env):
    """Set the document language for pages explicitly marked as English."""
    docs_dir = env.conf['docs_dir']
    site_dir = env.conf['site_dir']
    for root, _, filenames in os.walk(docs_dir):
        for filename in filenames:
            if not filename.endswith('.md'):
                continue
            source = os.path.join(root, filename)
            with open(source, 'r', encoding='utf-8') as file:
                metadata = extract_metadata(file.read())
            if not metadata.get('english', False):
                continue

            relative = os.path.relpath(source, docs_dir)
            output_relative = os.path.splitext(relative)[0] + os.sep + 'index.html'
            output = os.path.join(site_dir, output_relative)
            if not os.path.isfile(output):
                continue
            with open(output, 'r', encoding='utf-8') as file:
                rendered = file.read()
            rendered = rendered.replace('<html lang="fa"', '<html lang="en"', 1)
            with open(output, 'w', encoding='utf-8', newline='') as file:
                file.write(rendered)

import os
import re

def extract_metadata(content):
    metadata = {}
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        for line in yaml_text.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip().strip('"').strip("'")
    return metadata

def define_env(env):
    @env.macro
    def get_recent_posts(base_folder="posts", limit=6):
        docs_dir = env.conf['docs_dir']
        target_dir = os.path.join(docs_dir, base_folder)
        
        if not os.path.exists(target_dir):
            return f"<p style='color:var(--crimson);'>پوشه {base_folder} یافت نشد.</p>"

        posts = []
        for root, dirs, files in os.walk(target_dir):
            for filename in files:
                if filename.endswith('.md') and filename != 'index.md':
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    metadata = extract_metadata(content)
                    
                    if metadata:
                        rel_dir = os.path.relpath(root, docs_dir).replace('\\', '/')
                        url_path = f"{rel_dir}/{filename.replace('.md', '/')}"
                        
                        posts.append({
                            'title': metadata.get('title', 'بدون عنوان'),
                            'category': metadata.get('category', 'عمومی'),
                            'date': metadata.get('date', 'بدون تاریخ'),
                            'excerpt': metadata.get('excerpt', '...'),
                            'image': metadata.get('image', ''), # گرفتن آدرس عکس
                            'url': url_path
                        })
        
        posts.sort(key=lambda x: x['date'], reverse=True)
        
        html = '<div class="post-grid">\n'
        for post in posts[:limit]:
            # تغییر جدید: اگر عکسی نبود، از عکس پیش‌فرض استفاده کن
            img_src = post['image'] if post['image'] else 'assets/images/default-cover.svg'
            image_html = f'<div class="post-card-image"><img src="{img_src}" alt="{post["title"]}"></div>'
            
            html += f"""
            <a href="{post['url']}" class="post-card">
                {image_html}
                <div class="post-card-content">
                    <span class="post-category">{post['category']}</span>
                    <h3>{post['title']}</h3>
                    <p class="post-excerpt">{post['excerpt']}</p>
                    <div class="post-meta">
                        <span>{post['date']}</span>
                        <span>خواندن</span>
                    </div>
                </div>
            </a>
            """
        html += '</div>\n'
        
        return html
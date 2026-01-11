import os
import re
import urllib.request

dir_path = 'source/_posts'
image_dir = 'source/images'
os.makedirs(image_dir, exist_ok=True)

def download_image(url, filepath):
    try:
        urllib.request.urlretrieve(url, filepath)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

for filename in os.listdir(dir_path):
    if filename.endswith('.md'):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all image markdown ![alt](url)
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        matches = re.findall(pattern, content)
        
        for alt, url in matches:
            if url.startswith('https://') and 'csdnimg.cn' in url:
                img_filename = url.split('/')[-1]
                img_filepath = os.path.join(image_dir, img_filename)
                if not os.path.exists(img_filepath):
                    print(f"Downloading {url}")
                    download_image(url, img_filepath)
                new_url = f'./images/{img_filename}'
                old_markdown = f'![{alt}]({url})'
                new_markdown = f'![{alt}]({new_url})'
                content = content.replace(old_markdown, new_markdown)
        
        # Write back if changed
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Processed {filename}')

print('Done')
import os
import re

dir_path = 'source/_posts'

for filename in os.listdir(dir_path):
    if filename.endswith('.md'):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace csdnimg.cn links with ./images/
        content = re.sub(r'https://[^)]*csdnimg\.cn/([^)]+)', r'./images/\1', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'Processed {filename}')

print('Done')
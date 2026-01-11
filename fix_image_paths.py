import os
import re

dir_path = 'source/_posts'

for filename in os.listdir(dir_path):
    if filename.endswith('.md'):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace /images with ./images
        content = content.replace('/images/', './images/')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'Updated {filename}')

print('Done')
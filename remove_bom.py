import os

dir_path = 'source/_posts'

for filename in os.listdir(dir_path):
    if filename.endswith('.md'):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM at beginning
            content = f.read()
        # Remove any remaining BOM characters in the content
        content = content.replace('\ufeff', '')
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Removed BOM from {filename}')

print('Done')
import os
import re

dir_path = 'source/_posts'
date = '2026-01-11 15:30:00'
layout = 'post'

tags_dict = {
    'IC设计': '[IC设计]',
    '操作系统': '[操作系统, RISC-V,嵌入式软件开发]',
    '程序人生': '[程序人生]',
    '读书笔记': '[读书笔记]',
    '安装配置': '[安装配置]',
    '异常处理': '[异常处理]',
    '片上网络专题讨论一': '[片上网络]',
    'OFDM系列': '[OFDM, 通信]',
    '环境配置': '[环境配置]',
}

for filename in os.listdir(dir_path):
    if filename.endswith('.md'):
        filepath = os.path.join(dir_path, filename)
        title = filename[:-3]  # remove .md
        match = re.match(r'【(.+?)】(.+)', title)
        if match:
            categories = match.group(1).strip()
            title_body = match.group(2).strip()
        else:
            categories = ''
            title_body = title
        # Special cases
        if 'PyTorch' in title:
            tags = '[PyTorch, 深度学习]'
        elif 'hello-world' in title:
            tags = '[]'
        else:
            tags = tags_dict.get(categories, f'[{categories}]' if categories else '[]')
        # Front matter
        front_matter = f'''---
title: {title}
date: {date}
categories: {categories}
tags: {tags}
layout: {layout}
---
'''
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Check if already has front matter
        if content.startswith('---'):
            print(f'Skipping {filename}, already has front matter')
        else:
            # Add front matter
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(front_matter + content)
            print(f'Updated {filename}')

print('Done')
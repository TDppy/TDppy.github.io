import requests
from bs4 import BeautifulSoup
import re
import os

url = 'https://blog.csdn.net/qq_42622433?type=blog'
response = requests.get(url)
with open('csdn.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

# Fetch from category pages
date_map = {}
category_urls = [
    'https://blog.csdn.net/qq_42622433/category_11752459.html',
    'https://blog.csdn.net/qq_42622433/category_11973980.html',
    'https://blog.csdn.net/qq_42622433/category_13114364.html',
    'https://blog.csdn.net/qq_42622433/category_9609764.html',
    'https://blog.csdn.net/qq_42622433/category_13032097.html',
    'https://blog.csdn.net/qq_42622433/category_9609771.html',
    'https://blog.csdn.net/qq_42622433/category_9709395.html',
    'https://blog.csdn.net/qq_42622433/category_9947788.html',
    'https://blog.csdn.net/qq_42622433/category_9862290.html',
    'https://blog.csdn.net/qq_42622433/category_9609773.html',
    'https://blog.csdn.net/qq_42622433/category_12412440.html',
    'https://blog.csdn.net/qq_42622433/category_11412838.html',
    'https://blog.csdn.net/qq_42622433/category_9674582.html',
    'https://blog.csdn.net/qq_42622433/category_11181680.html',
    'https://blog.csdn.net/qq_42622433/category_9609767.html',
    'https://blog.csdn.net/qq_42622433/category_10201240.html',
    'https://blog.csdn.net/qq_42622433/category_9525596.html',
    'https://blog.csdn.net/qq_42622433/category_10170058.html',
    'https://blog.csdn.net/qq_42622433/category_10121016.html'
]

for url in category_urls[:1]:  # test with first
    response = requests.get(url)
    with open('category.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='blog-list-box')
    print(f"Found {len(articles)} articles")
    for article in articles[:5]:  # first 5
        title_elem = article.find('h4')
        if title_elem:
            title = title_elem.get_text(strip=True)
            print(f"Title: {title}")
            time_elem = article.find('div', class_='view-time-box')
            if time_elem:
                time_text = time_elem.get_text(strip=True)
                print(f"Time: {time_text}")
                match = re.search(r'(\d{4})\.(\d{2})\.(\d{2})', time_text)
                if match:
                    year, month, day = match.groups()
                    formatted_date = f'{year}-{month}-{day} 15:30:00'
                    date_map[title] = formatted_date
                    print(f"Date: {formatted_date}")
print(f"Collected {len(date_map)} dates")

# Now, update local files
posts_dir = 'source/_posts'
for f in os.listdir(posts_dir):
    if f.endswith('.md'):
        path = os.path.join(posts_dir, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        title_match = re.search(r'title: (.+)', content)
        if title_match:
            title = title_match.group(1).strip()
            if title in date_map:
                # Update date
                content = re.sub(r'date: .+', f'date: {date_map[title]}', content)
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f'Updated {f} with date {date_map[title]}')

print('Done')
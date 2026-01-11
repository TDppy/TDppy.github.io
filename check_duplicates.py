import os

image_dir = 'source/_posts/images'
files = os.listdir(image_dir)

file_count = {}
for f in files:
    if os.path.isfile(os.path.join(image_dir, f)):
        file_count[f] = file_count.get(f, 0) + 1

duplicates = [f for f, count in file_count.items() if count > 1]

if duplicates:
    print("Duplicate images found:")
    for dup in duplicates:
        print(f"{dup}: {file_count[dup]} times")
else:
    print("No duplicate images found.")
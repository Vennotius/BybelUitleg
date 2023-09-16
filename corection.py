import json
import re

def contains_two_words_separated_by_dot(input_str):
    pattern = r'\b(\w+)\.(\w+)\b'
    matches = re.findall(pattern, input_str)
    return bool(matches)

def add_space_after_dot(input_str):
    pattern = r'\b(\w+)\.(\w+)\b'
    replacement = r'\1. \2'
    modified_str = re.sub(pattern, replacement, input_str)
    return modified_str

# Load JSON
with open('Bybel.json', 'r', encoding='utf-8') as f:
    BYBEL_TEKS = json.loads(f.read())

# Iterate through the structure
for book_index, book in enumerate(BYBEL_TEKS):
    for chapter_index, chapter in enumerate(book):
        for verse_index, verse in enumerate(chapter):
            if contains_two_words_separated_by_dot(verse):
                modified_verse = add_space_after_dot(verse)
                
                # Replace the verse in the list
                BYBEL_TEKS[book_index][chapter_index][verse_index] = modified_verse
                
                print(verse)
                print(modified_verse)

# Save the modified JSON
with open('Bybel_20230916.json', 'w', encoding='utf-8') as f:
    json.dump(BYBEL_TEKS, f, ensure_ascii=False, indent=4)

print('--------------------------')
print('--------------------------')

# Load JSON
with open('Bybel_20230916.json', 'r', encoding='utf-8') as f:
    BYBEL_TEKS = json.loads(f.read())

# Iterate through the structure
for book_index, book in enumerate(BYBEL_TEKS):
    for chapter_index, chapter in enumerate(book):
        for verse_index, verse in enumerate(chapter):
            if contains_two_words_separated_by_dot(verse):
                modified_verse = add_space_after_dot(verse)
                
                # Replace the verse in the list
                BYBEL_TEKS[book_index][chapter_index][verse_index] = modified_verse
                
                print(verse)
                print(modified_verse)
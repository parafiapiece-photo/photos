import os
import json
from datetime import datetime

IMAGE_EXTENSIONS = ('.webp', '.jpg', '.jpeg', '.png')
BASE_DIR = '.' 
OUTPUT_FILE = 'galleries.json'

def generate_galleries():
    galleries = []
    
    # Pobieramy foldery lat i sortujemy malejąco
    years = [d for d in os.listdir(BASE_DIR) if d.isdigit() and len(d) == 4]
    years.sort(reverse=True)

    for year in years:
        year_path = os.path.join(BASE_DIR, year)
        # Pobieramy wydarzenia w danym roku
        events = [d for d in os.listdir(year_path) if os.path.isdir(os.path.join(year_path, d))]
        events.sort(reverse=True)

        for event in events:
            event_path = os.path.join(year, event)
            full_path = os.path.join(BASE_DIR, event_path)
            
            # Lista zdjęć
            images = [f for f in os.listdir(full_path) if f.lower().endswith(IMAGE_EXTENSIONS)]
            images.sort()

            if not images:
                continue

            # Logika daty i tytułu
            try:
                date_str = event.split('_')[0]
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                date_str = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d')

            title = event.split('_')[-1].replace('-', ' ').replace('_', ' ').capitalize()

            gallery = {
                "id": event.replace('.', '-'),
                "title": title,
                "date": date_str,
                "folder": event_path,
                "coverImage": images[0],
                "photos": images
            }
            
            galleries.append(gallery)
            print(f"Dodano: {year} -> {title} ({len(images)} zdjęć)")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(galleries, f, indent=2, ensure_ascii=False)

    print(f"\nSukces! Wygenerowano {len(galleries)} galerii w {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_galleries()

import os
import json
from datetime import datetime

IMAGE_EXTENSIONS = ('.webp', '.jpg', '.jpeg', '.png')
BASE_DIR = '.' 
OUTPUT_FILE = 'galleries.json'

def get_images_in_dir(directory):
    if not os.path.exists(directory):
        return []
    images = [f for f in os.listdir(directory) if f.lower().endswith(IMAGE_EXTENSIONS)]
    images.sort()
    return images

def generate_galleries():
    galleries = []
    current_year = datetime.now().year

    # 1. FOLDER SPECJALNY "KOSCIOL"
    special_folder = 'kosciol'
    if os.path.isdir(special_folder):
        images = get_images_in_dir(special_folder)
        if images:
            galleries.append({
                "id": "nasz-kosciol",
                "title": f"Wnętrze kościoła {current_year}",
                "date": f"{current_year}-01",
                "folder": special_folder,
                "coverImage": images[0],
                "photos": images
            })
            print(f"Dodano folder specjalny: {special_folder}")

    # 2. SKANOWANIE LAT
    years = [d for d in os.listdir(BASE_DIR) if d.isdigit() and len(d) == 4]
    years.sort(reverse=True)

    for year in years:
        year_path = os.path.join(BASE_DIR, year)
        events = [d for d in os.listdir(year_path) if os.path.isdir(os.path.join(year_path, d))]
        events.sort(reverse=True)

        for event in events:
            event_rel_path = os.path.join(year, event)
            full_path = os.path.join(BASE_DIR, event_rel_path)
            
            images = get_images_in_dir(full_path)
            if not images:
                continue

            # Tytuł: Nazwa folderu + Rok (np. "Wielkanoc 2021")
            clean_name = event.replace('-', ' ').replace('_', ' ').capitalize()
            display_title = f"{clean_name} {year}"
            
            # Unikalne ID
            unique_id = f"{year}-{event.replace('_', '-')}"

            galleries.append({
                "id": unique_id,
                "title": display_title,
                "date": f"{year}-01",
                "folder": event_rel_path,
                "coverImage": images[0],
                "photos": images
            })
            print(f"Dodano: {display_title}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(galleries, f, indent=2, ensure_ascii=False)
    
    print(f"\nGotowe! Wygenerowano {len(galleries)} galerii.")

if __name__ == "__main__":
    generate_galleries()

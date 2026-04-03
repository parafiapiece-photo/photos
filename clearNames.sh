#!/bin/bash

# Funkcja czyszcząca nazwę
clean_name() {
    local name="$1"
    # 1. Zamień spacje na podkreślniki
    # 2. Usuń znaki specjalne (zostaw litery, cyfry, _, -, .)
    # 3. Zamień wielokrotne podkreślniki na jeden
    echo "$name" | sed 's/ /_/g' | sed 's/[^a-zA-Z0-9._-]//g' | sed 's/_\+/_/g'
}

# Najpierw zmień nazwy plików (najgłębiej)
find . -type f | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    cleaned=$(clean_name "$base")
    if [ "$base" != "$cleaned" ]; then
        mv "$dir/$base" "$dir/$cleaned"
        echo "Plik: $base -> $cleaned"
    fi
done

# Potem zmień nazwy folderów
find . -type d -not -path '*/.*' | sort -r | while read -r dir; do
    parent=$(dirname "$dir")
    base=$(basename "$dir")
    cleaned=$(clean_name "$base")
    if [ "$base" != "$cleaned" ]; then
        mv "$parent/$base" "$parent/$cleaned"
        echo "Folder: $base -> $cleaned"
    fi
done

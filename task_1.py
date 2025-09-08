"""
Завдання 1:

Напишіть програму на Python, яка рекурсивно копіює файли у вихідній директорії, переміщає їх до нової директорії 
та сортує в піддиректорії, назви яких базуються на розширенні файлів.

Також візьміть до уваги наступні умови:

1. Парсинг аргументів. Скрипт має приймати два аргументи командного рядка: шлях до вихідної директорії 
та шлях до директорії призначення (за замовчуванням, якщо тека призначення не була передана, вона повинна бути з назвою dist).

2. Рекурсивне читання директорій:

Має бути написана функція, яка приймає шлях до директорії як аргумент.
Функція має перебирати всі елементи у директорії.
Якщо елемент є директорією, функція повинна викликати саму себе рекурсивно для цієї директорії.
Якщо елемент є файлом, він має бути доступним для копіювання.
3. Копіювання файлів:

Для кожного типу файлів має бути створений новий шлях у вихідній директорії, використовуючи розширення файлу для назви піддиректорії.
Файл з відповідним типом має бути скопійований у відповідну піддиректорію.
4. Обробка винятків. Код має правильно обробляти винятки, наприклад, помилки доступу до файлів або директорій.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

def extension_folder_for(path: Path) -> str:
    suffixes = [s.lstrip(".").lower() for s in path.suffixes if s]
    return ".".join(suffixes) if suffixes else "no_ext"

def unique_target_path(target_dir: Path, src_name: str) -> Path:
    
    candidate = target_dir / src_name
    if not candidate.exists():
        return candidate
    stem, suffix = candidate.stem, candidate.suffix
    i = 1
    while True:
        alt = target_dir / f"{stem} ({i}){suffix}"
        if not alt.exists():
            return alt
        i += 1

def copy_all(source: Path, dest_root: Path) -> tuple[int, int]:
    """
    Рекурсивно копіює всі файли з source у dest_root/<ext>/...
    Повертає (copied, skipped).
    """
    copied = 0
    skipped = 0

    source_abs = source.resolve()
    dest_abs = dest_root.resolve()

    for current_root, dirs, files in os.walk(source_abs):
        root_path = Path(current_root)

        # Якщо dest всередині source — не заходимо туди під час обходу
        dirs[:] = [d for d in dirs if (root_path / d).resolve() != dest_abs]

        for name in files:
            src = root_path / name
            ext_folder = extension_folder_for(src)
            target_dir = dest_abs / ext_folder

            try:
                target_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                print(f"Cannot create dir {target_dir}: {e}", file=sys.stderr)
                skipped += 1
                continue

            dst = unique_target_path(target_dir, src.name)

            try:
                shutil.copy2(src, dst)
                print(f"{src.relative_to(source_abs)} -> {dst.relative_to(dest_abs)}")
                copied += 1
            except (PermissionError, OSError, shutil.Error) as e:
                print(f"Failed to copy {src}: {e}", file=sys.stderr)
                skipped += 1

    return copied, skipped

def main():
    parser = argparse.ArgumentParser(
        description="Copy files from SOURCE_DIR into DEST_DIR, sorted by file extension."
    )
    # перший аргумент – обов’язковий
    parser.add_argument("source", type=Path, help="Path to the source directory.")
    # другий – необов’язковий, за замовчуванням 'dist'
    parser.add_argument(
        "dest",
        nargs="?",
        default=Path("dist"),
        type=Path,
        help='Path to the destination directory (default: "dist").'
    )
    args = parser.parse_args()

    # Перевіряємо чи існує ця директорія, і що це саме директорія
    if not args.source.exists():
        parser.error(f"Source not found: {args.source}")
    if not args.source.is_dir():
        parser.error(f"Source is not a directory: {args.source}")

    try:
        args.dest.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        parser.error(f"Cannot create destination directory {args.dest}: {e}")

    print(f"SOURCE: {args.source.resolve()}")
    print(f"DEST:   {args.dest.resolve()}\n")

    copied, skipped = copy_all(args.source, args.dest)
    print(f"\nDone. Copied: {copied}, skipped: {skipped}. Output: {args.dest.resolve()}")

if __name__ == "__main__":
    main()

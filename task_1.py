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


def copy_recursive(current: Path, dest_root: Path, src_root: Path) -> tuple[int, int]:
    """Мінімалістична рекурсія в стилі display_tree: тека → рекурсія, файл → копіюємо."""
    copied = skipped = 0
    dest_abs = dest_root.resolve()

    try:
        children = sorted(current.iterdir(), key=lambda p: (p.is_file(), p.name))
    except OSError as e:
        print(f"Cannot access {current}: {e}", file=sys.stderr)
        return 0, 1

    for item in children:
        try:
            if item.is_dir():
                # не заходимо у теку призначення, якщо вона всередині source
                if item.resolve() == dest_abs:
                    continue
                c, s = copy_recursive(item, dest_root, src_root)
                copied += c
                skipped += s
            elif item.is_file():
                ext_dir = dest_root / extension_folder_for(item)
                try:
                    ext_dir.mkdir(parents=True, exist_ok=True)
                    dst = unique_target_path(ext_dir, item.name)
                    shutil.copy2(item, dst)
                    print(
                        f"{item.relative_to(src_root)} -> {dst.relative_to(dest_root)}"
                    )
                    copied += 1
                except (OSError, shutil.Error) as e:
                    print(f"Failed to copy {item}: {e}", file=sys.stderr)
                    skipped += 1
            else:
                skipped += 1  # спецфайли/невідомі типи
        except OSError as e:
            print(f"Failed on {item}: {e}", file=sys.stderr)
            skipped += 1

    return copied, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Copy files from SOURCE_DIR into DEST_DIR, sorted by file extension."
    )
    parser.add_argument("source", type=Path, help="Path to the source directory.")
    parser.add_argument(
        "dest",
        nargs="?",
        default=Path("dist"),
        type=Path,
        help='Path to the destination directory (default: "dist").',
    )
    args = parser.parse_args()

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

    copied, skipped = copy_recursive(
        args.source.resolve(), args.dest.resolve(), args.source.resolve()
    )
    print(
        f"\nDone. Copied: {copied}, skipped: {skipped}. Output: {args.dest.resolve()}"
    )


if __name__ == "__main__":
    main()

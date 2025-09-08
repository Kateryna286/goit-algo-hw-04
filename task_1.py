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
from pathlib import Path

def extension_folder_for(path: Path) -> str:
    """Повертає назву підпапки за розширенням файлу."""
    suffixes = [s.lstrip(".").lower() for s in path.suffixes if s]
    return ".".join(suffixes) if suffixes else "no_ext"

def walk_dir(root: Path) -> None:
    """
    Рекурсивно обходить root і друкує:
      <відносний_шлях_файлу> -> <папка_за_розширенням>
    """
    root = root.resolve()
    for current_root, dirs, files in os.walk(root):
        base = Path(current_root)
        for name in files:
            file_path = base / name
            rel = file_path.relative_to(root)
            target = extension_folder_for(file_path)
            print(f"{rel} -> {target}")

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

    # Показуємо, що знайдемо
    print(f"SOURCE: {args.source.resolve()}")
    print(f"DEST:   {args.dest.resolve()}\n")

    walk_dir(args.source)

if __name__ == "__main__":
    main()

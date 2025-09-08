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
from pathlib import Path

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

    print(f"SOURCE: {args.source}")
    print(f"DEST:   {args.dest}")

if __name__ == "__main__":
    main()



# COLOR_BLUE = "\033[94m"
# COLOR_GREEN = "\033[92m"
# COLOR_RESET = "\033[0m"

# def display_tree(path: Path, indent: str = "", prefix: str = "") -> None:
#     if path.is_dir():
#         # Use blue color for directories
#         print(indent + prefix + COLOR_BLUE + str(path.name) + COLOR_RESET)
#         indent += "    " if prefix else ""

#         # Get a sorted list of children, with directories last
#         children = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))

#         for index, child in enumerate(children):
#             # Check if the current child is the last one in the directory
#             is_last = index == len(children) - 1
#             display_tree(child, indent, "└── " if is_last else "├── ")
#     else:
#         print(indent + prefix + COLOR_GREEN + str(path.name) + COLOR_RESET)

# if __name__ == "__main__":
#     root = Path("test_data")
#     display_tree(root)

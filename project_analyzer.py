import os
import argparse
from pathlib import Path


def get_project_structure(root_dir, prefix="", ignore_dirs=None):
    """Рекурсивно строит структуру проекта"""
    if ignore_dirs is None:
        ignore_dirs = {
            ".git",
            "__pycache__",
            ".vscode",
            ".idea",
            ".venv",
            ".ruff_cache",
            "env",
            "node_modules",
        }

    structure = []
    try:
        items = sorted(
            [item for item in os.listdir(root_dir) if item not in ignore_dirs]
        )
    except PermissionError:
        return []

    for i, item in enumerate(items):
        item_path = os.path.join(root_dir, item)
        is_last = i == len(items) - 1

        connector = "└── " if is_last else "├── "

        if os.path.isdir(item_path):
            structure.append(prefix + connector + item + "/")
            extension = "    " if is_last else "│   "
            structure.extend(
                get_project_structure(item_path, prefix + extension, ignore_dirs)
            )
        else:
            structure.append(prefix + connector + item)

    return structure


def extract_py_files_content(root_dir, output_file):
    """Рекурсивно извлекает содержимое всех .py файлов"""
    with open(output_file, "w", encoding="utf-8") as outfile:
        # Структура проекта
        outfile.write("СТРУКТУРА ПРОЕКТА:\n")
        outfile.write("=================\n")
        structure = get_project_structure(root_dir)
        for line in structure:
            outfile.write(line + "\n")

        outfile.write("\n" + "=" * 80 + "\n")
        outfile.write("СОДЕРЖИМОЕ .py ФАЙЛОВ:\n")
        outfile.write("=" * 80 + "\n\n")

        # Содержимое .py файлов
        for root, dirs, files in os.walk(root_dir):
            # Игнорируем служебные папки и сам этот скрипт
            dirs[:] = [
                d
                for d in dirs
                if d
                not in {
                    ".git",
                    "__pycache__",
                    ".vscode",
                    ".idea",
                    ".venv",
                    "env",
                    "node_modules",
                }
            ]

            for file in files:
                if file.endswith(".py") and file != os.path.basename(__file__):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, root_dir)

                    try:
                        with open(file_path, "r", encoding="utf-8") as infile:
                            content = infile.read()

                        outfile.write(f"\n{'=' * 60}\n")
                        outfile.write(f"ФАЙЛ: {relative_path}\n")
                        outfile.write(f"{'=' * 60}\n\n")
                        outfile.write(content)

                        if not content.endswith("\n"):
                            outfile.write("\n")

                    except Exception as e:
                        outfile.write(
                            f"\nОШИБКА при чтении {relative_path}: {str(e)}\n"
                        )

    print(f"✅ Результат сохранен в: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Анализ структуры проекта и извлечение .py файлов"
    )
    parser.add_argument(
        "--root", "-r", default=".", help="Корневая директория (по умолчанию: текущая)"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="project_analysis.txt",
        help="Выходной файл (по умолчанию: project_analysis.txt)",
    )

    args = parser.parse_args()

    root_dir = os.path.abspath(args.root)

    if not os.path.exists(root_dir):
        print(f"❌ Ошибка: Директория '{root_dir}' не существует!")
        return

    print(f"🔍 Анализируем проект: {root_dir}")
    extract_py_files_content(root_dir, args.output)


if __name__ == "__main__":
    main()

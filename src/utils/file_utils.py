import os
from typing import List, Optional, Set
from pathlib import Path
import fnmatch
import shutil

from .config import LANGUAGE_CONFIG, IGNORE_PATTERNS, MAX_FILE_SIZE


def get_files_in_directory(directory: str, extensions: Optional[List[str]] = None) -> List[str]:
    """Отримання списоку файлів у директорії з розширеннями

    Args:
        directory: Шлях до директорії
        extensions: Список розширень файлів для фільтрації (None для всіх файлів)

    Returns:
        Список шляхів до знайдених файлів
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        #Фільтрування ігнорованих директорій
        dirs[:] = [d for d in dirs if not should_ignore(d)]

        for file in files:
            if should_ignore(file):
                continue

            file_path = os.path.join(root, file)

            #Перевірка розміру файлу
            if os.path.getsize(file_path) > MAX_FILE_SIZE:
                continue

            if extensions:
                if any(file.endswith(ext) for ext in extensions):
                    file_list.append(file_path)
            else:
                file_list.append(file_path)
    return file_list


def create_directory(path: str) -> None:
    """Створення директорії, якщо її не існує

    Args:
        path: Шлях до директорії
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def is_source_code_file(file_path: str) -> bool:
    """Перевірка, чи є файл файлом вихідного коду

    Args:
        file_path: Шлях до файлу

    Returns:
        True, якщо файл є файлом вихідного коду, інакше False
    """
    extensions = [ext for lang in LANGUAGE_CONFIG.values() for ext in lang['extensions']]
    return any(file_path.endswith(ext) for ext in extensions)


def should_ignore(path: str) -> bool:
    """Перевірка, чи слід ігнорувати файл або директорію

    Args:
        path: Шлях до файлу або директорії

    Returns:
        True, якщо шлях слід ігнорувати, інакше False
    """
    return any(fnmatch.fnmatch(path, pattern) for pattern in IGNORE_PATTERNS)


def copy_file(src: str, dest: str) -> None:
    """Копіювати файл з збереженням метаданих

    Args:
        src: Шлях до вихідного файлу
        dest: Шлях до цільового файлу
    """
    try:
        shutil.copy2(src, dest)
    except (shutil.SameFileError, PermissionError) as e:
        print(f"Помилка копіювання {src}: {str(e)}")


def move_file(src: str, dest: str) -> None:
    """Перемістити файл

    Args:
        src: Шлях до вихідного файлу
        dest: Шлях до цільового файлу
    """
    try:
        shutil.move(src, dest)
    except (shutil.SameFileError, PermissionError) as e:
        print(f"Помилка переміщення {src}: {str(e)}")


def count_lines_in_file(file_path: str) -> int:
    """Підрахунок кількості рядків у файлі

    Args:
        file_path: Шлях до файлу

    Returns:
        Кількість рядків у файлі
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return sum(1 for _ in file)
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return sum(1 for _ in file)
        except Exception:
            return 0
    except Exception:
        return 0


def get_all_source_code_extensions() -> Set[str]:
    """Отримання всіх розширень файлів вихідного коду

    Returns:
        Множина всіх розширень файлів вихідного коду
    """
    return {ext for lang in LANGUAGE_CONFIG.values() for ext in lang['extensions']}
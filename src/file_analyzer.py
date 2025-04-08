import os
import re
import mimetypes
import logging
import chardet
from collections import defaultdict
from datetime import datetime


class FileAnalyzer:
    """Клас для аналізу та категоризації файлів"""

    def __init__(self):
        """Ініціалізація файлового аналізатора"""
        self.logger = logging.getLogger(__name__)
        #Ініціалізація міметипів
        mimetypes.init()

    def determine_file_category(self, file_path, category_rules):
        """
        Визначення категорії файлу на основі правил

        Args:
            file_path (str): Шлях до файлу
            category_rules (dict): Словник з назвами категорій як ключами та правилами як значеннями

        Returns:
            str: Назва категорії або None якщо немає збігу категорій
        """
        if not os.path.isfile(file_path):
            return None

        filename = os.path.basename(file_path)
        extension = os.path.splitext(filename)[1].lower()

        #Спроба визначити міметипів
        mime_type, _ = mimetypes.guess_type(file_path)

        #Перегляд кожної категорії і перевірка, чи відповідає файл правилам
        for category, rules in category_rules.items():
            #Перевірка відповідністі розширення
            if "extensions" in rules and extension[1:] in rules["extensions"]:
                return category

            #Перевірка шаблонів імен файлів
            if "patterns" in rules:
                for pattern in rules["patterns"]:
                    if re.search(pattern, filename, re.IGNORECASE):
                        return category

            #Перевірка міметипів
            if mime_type and "mime_types" in rules and mime_type in rules["mime_types"]:
                return category

        return None

    def get_file_info(self, file_path):
        """
        Отримання інформації про файл

        Args:
            file_path (str): Шлях до файлу

        Returns:
            dict: Словник з інформацією про файл
        """
        try:
            stat_info = os.stat(file_path)

            file_info = {
                "name": os.path.basename(file_path),
                "path": file_path,
                "size": stat_info.st_size,
                "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                "extension": os.path.splitext(file_path)[1].lower(),
            }

            #Отримання міметипів
            mime_type, encoding = mimetypes.guess_type(file_path)
            file_info["mime_type"] = mime_type

            #Спроба визначити мову для файлів коду
            file_info["language"] = self._detect_file_language(file_path)

            return file_info
        except Exception as e:
            self.logger.error(f"Error getting file info for {file_path}: {str(e)}")
            return None

    def _detect_file_language(self, file_path):
        """
        Визначення мови програмування файлу за розширенням

        Args:
            file_path (str): Шлях до файлу

        Returns:
            str: Визначена мова or None
        """
        extension = os.path.splitext(file_path)[1].lower()

        #Базове розширення для відображення мов
        ext_to_lang = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.java': 'Java',
            '.c': 'C',
            '.cpp': 'C++',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React',
            '.md': 'Markdown',
            '.json': 'JSON',
            '.xml': 'XML',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.bat': 'Batch',
            '.ps1': 'PowerShell'
        }

        return ext_to_lang.get(extension)

    def get_directory_statistics(self, file_paths):
        """
        Отримання статистики файлів в директорії

        Args:
            file_paths (list): Список шляхів до файлів

        Returns:
            dict: Словник зі статистикою
        """
        stats = {
            "total_files": len(file_paths),
            "total_size": 0,
            "extensions": defaultdict(int),
            "mime_types": defaultdict(int),
            "language_breakdown": defaultdict(int),
            "language_stats": defaultdict(lambda: {
                "file_count": 0,
                "total_size": 0,
                "total_lines": 0,
                "average_size": 0,
                "average_lines": 0,
                "largest_file": "",
                "extensions": set()
            }),
            "oldest_file": None,
            "newest_file": None,
            "largest_file": None,
            "average_size": 0,
            "total_lines": 0,
            "average_lines": 0,
            "largest_files": [],
            "newest_files": []
        }

        if not file_paths:
            return stats

        oldest_time = None
        newest_time = None
        largest_size = 0
        all_file_infos = []

        for file_path in file_paths:
            try:
                file_info = self.get_file_info(file_path)
                if not file_info:
                    continue

                all_file_infos.append(file_info)

                #Оновлення базової статистики
                stats["total_size"] += file_info["size"]
                extension = file_info["extension"]
                stats["extensions"][extension] += 1

                #Підрахування рядків, якщо це текстовий файл
                lines = 0
                if self._is_text_file(file_path):
                    lines = self._count_lines(file_path)
                    stats["total_lines"] += lines

                #Оновлення мовної статистики
                language = file_info.get("language", "Unknown")
                if language:
                    stats["language_breakdown"][language] += 1

                    #Оновлення детальної мовної статистики
                    lang_stats = stats["language_stats"][language]
                    lang_stats["file_count"] += 1
                    lang_stats["total_size"] += file_info["size"]
                    lang_stats["total_lines"] += lines
                    lang_stats["extensions"].add(extension)

                    #Перевірка, чи це найбільший файл для цієї мови
                    if not lang_stats["largest_file"] or file_info["size"] > os.path.getsize(
                            lang_stats["largest_file"]):
                        lang_stats["largest_file"] = file_path

                if file_info["mime_type"]:
                    stats["mime_types"][file_info["mime_type"]] += 1

                #Перевірка найстарішого файлу
                file_time = datetime.fromisoformat(file_info["modified"])
                if oldest_time is None or file_time < oldest_time:
                    oldest_time = file_time
                    stats["oldest_file"] = file_info

                #Перевірка найновішого файлу
                if newest_time is None or file_time > newest_time:
                    newest_time = file_time
                    stats["newest_file"] = file_info

                #Перевірка найбільшого файлу
                if file_info["size"] > largest_size:
                    largest_size = file_info["size"]
                    stats["largest_file"] = file_info

            except Exception as e:
                self.logger.error(f"Error processing file {file_path}: {str(e)}")

        #Обчислення середніх значень і сортування списків
        if stats["total_files"] > 0:
            stats["average_size"] = stats["total_size"] / stats["total_files"]
            if stats["total_lines"] > 0:
                stats["average_lines"] = stats["total_lines"] / stats["total_files"]

        #Обчислення середніх значень мови
        for lang, lang_stats in stats["language_stats"].items():
            if lang_stats["file_count"] > 0:
                lang_stats["average_size"] = lang_stats["total_size"] / lang_stats["file_count"]
                if lang_stats["total_lines"] > 0:
                    lang_stats["average_lines"] = lang_stats["total_lines"] / lang_stats["file_count"]
                lang_stats["extensions"] = list(lang_stats["extensions"])

        #Сортування інформації про файл для найбільших і найновіших файлів
        sorted_by_size = sorted(all_file_infos, key=lambda x: x["size"], reverse=True)
        stats["largest_files"] = sorted_by_size[:10]

        sorted_by_date = sorted(all_file_infos, key=lambda x: x["modified"], reverse=True)
        stats["newest_files"] = sorted_by_date[:10]

        return stats

    def _is_text_file(self, file_path):
        """Перевірка, чи файл є текстовим"""
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type and mime_type.startswith('text/'):
            return True

        #Додаткова перевірка файлів вихідного коду
        ext = os.path.splitext(file_path)[1].lower()
        code_extensions = ['.py', '.js', '.html', '.css', '.java', '.c', '.cpp', '.cs',
                           '.php', '.rb', '.go', '.ts', '.jsx', '.tsx', '.md', '.json',
                           '.xml', '.sql', '.sh', '.bat', '.ps1']
        if ext in code_extensions:
            return True

        #Спроба визначення кодування в крайньому випадку
        try:
            with open(file_path, 'rb') as f:
                sample = f.read(4096)
                result = chardet.detect(sample)
                if result['encoding'] and result['confidence'] > 0.7:
                    return True
        except:
            pass

        return False

    def _count_lines(self, file_path):
        """Підрахування кількісті рядків у файлі"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sum(1 for _ in f)
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return sum(1 for _ in f)
            except:
                return 0
        except:
            return 0

    def find_duplicate_files(self, file_paths):
        """
        Пошук дублікатів файлів за розміром та іменем

        Args:
            file_paths (list): Список шляхів до файлів

        Returns:
            dict: Словник з повторюваними файлами, згрупованими за розміром, а потім за назвою
        """
        #Групування файлів за розміром
        files_by_size = defaultdict(list)

        for file_path in file_paths:
            try:
                stat_info = os.stat(file_path)
                size = stat_info.st_size
                files_by_size[size].append(file_path)
            except Exception as e:
                self.logger.error(f"Error processing file {file_path}: {str(e)}")

        #Пошук дублікатів
        duplicates = {}

        for size, files in files_by_size.items():
            if len(files) > 1:
                #Групування за ім'ям
                files_by_name = defaultdict(list)

                for file_path in files:
                    name = os.path.basename(file_path)
                    files_by_name[name].append(file_path)

                #Додавання до дублікатів, якщо є кілька файлів з однаковими іменами
                for name, name_files in files_by_name.items():
                    if len(name_files) > 1:
                        duplicates[f"{name} ({size} bytes)"] = name_files

        return duplicates

    def identify_file_patterns(self, file_paths, min_pattern_count=3):
        """
        Визначення загальних шаблонів в назвах файлів

        Args:
            file_paths (list): Список шляхів до файлів
            min_pattern_count (int): Мінімальна кількість файлів для розгляду шаблону

        Returns:
            dict: Словник зі зразками та відповідними файлами
        """
        #Витягнення дефолтних імен без розширень
        base_names = []

        for file_path in file_paths:
            filename = os.path.basename(file_path)
            base_name = os.path.splitext(filename)[0]
            base_names.append((base_name, file_path))

        #Пошук спільних закономірностей
        patterns = defaultdict(list)

        #Шаблон 1: Файли з числовими суфіксами типу «file1», «file2» і т.д.
        numeric_pattern = re.compile(r"^(.+?)(\d+)$")

        for base_name, file_path in base_names:
            match = numeric_pattern.match(base_name)
            if match:
                prefix = match.group(1)
                patterns[f"{prefix}[0-9]+"].append(file_path)

        #Відфільтровування шаблонів з меншою кількістю збігів, ніж min_pattern_count
        return {pattern: files for pattern, files in patterns.items()
                if len(files) >= min_pattern_count}

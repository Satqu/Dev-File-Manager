import os
import json
from typing import Dict, List, Any


class ConfigManager:
    def __init__(self, config_path=None):
        """Ініціалізує конфіг завдяки config path"""
        self.config_path = config_path

    def get_config(self) -> Dict[str, Any]:
        """Повертає конфіг зі структури file_categories"""
        return {
            "file_categories": self._get_file_categories(),
            "log_directory": "logs",
            "backup_directory": "backups",
            "ignore_patterns": IGNORE_PATTERNS
        }

    def _get_file_categories(self) -> Dict[str, Dict[str, List[str]]]:
        """Створює категорії файлів з правильною структурою правил для менеджменту файлів"""
        categories = {}

        #Генерація мовних категорій
        for lang, data in LANGUAGE_CONFIG.items():
            categories[lang] = {
                "extensions": [ext.lstrip('.') for ext in data["extensions"]],
                "patterns": data.get("signatures", [])
            }

        #Стандартні категорії
        categories.update({
            "Documents": {"extensions": ["pdf", "docx", "txt", "rtf", "md"]},
            "Images": {"extensions": ["jpg", "jpeg", "png", "gif", "bmp", "svg"]},
            "Archives": {"extensions": ["zip", "rar", "7z", "tar", "gz"]},
            "Data": {"extensions": ["csv", "json", "xlsx", "xml", "yml"]},
            "Other": {"extensions": ["*"]}  # Для всіх інших файлів
        })

        return categories

    def load_config(self) -> Dict[str, Any]:
        """Завантаження конфігу з JSON file"""
        if not self.config_path:
            return self.get_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл конфігу не знайдено: {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Неправильний JSON у файлі конфігу: {self.config_path}")

    @staticmethod
    def get_language_config():
        """Повертає словник мовних конфігів"""
        return LANGUAGE_CONFIG

    @staticmethod
    def get_ignore_patterns():
        """Повертає список ігнорованих шаблонів"""
        return IGNORE_PATTERNS

    @staticmethod
    def get_default_paths():
        """Повертає шлях до проєкту за замовчуванням"""
        return DEFAULT_PROJECTS_PATH, DEFAULT_ORGANIZED_PATH

    @staticmethod
    def get_file_settings():
        """Повертає налаштування файлів"""
        return MAX_FILE_SIZE, DEFAULT_ENCODING, FALLBACK_ENCODINGS


#Мовний конфіг
LANGUAGE_CONFIG: Dict[str, Dict[str, List[str]]] = {
    'Python': {
        'extensions': ['.py'],
        'signatures': ['def ', 'class ', 'import ', 'from '],
        'comment': '#'
    },
    'JavaScript': {
        'extensions': ['.js', '.jsx', '.ts', '.tsx'],
        'signatures': ['function ', 'const ', 'let ', 'import ', 'export '],
        'comment': '//'
    },
    'HTML': {
        'extensions': ['.html', '.htm'],
        'signatures': ['<!DOCTYPE', '<html', '<head', '<body'],
        'comment': '<!--'
    },
    'CSS': {
        'extensions': ['.css', '.scss', '.sass', '.less'],
        'signatures': ['body {', '@media', '#', '.'],
        'comment': '/*'
    },
    'C': {
        'extensions': ['.c', '.h'],
        'signatures': ['#include ', 'int ', 'void ', 'char ', 'float ', 'double '],
        'comment': '//'
    },
    'C++': {
        'extensions': ['.cpp', '.hpp', '.cc', '.cxx'],
        'signatures': ['#include ', 'class ', 'int ', 'void ', 'namespace '],
        'comment': '//'
    },
    'Java': {
        'extensions': ['.java'],
        'signatures': ['public class', 'import ', 'package ', 'public static void'],
        'comment': '//'
    },
    'PHP': {
        'extensions': ['.php'],
        'signatures': ['<?php', 'function ', 'class ', '$'],
        'comment': '//'
    },
    'Ruby': {
        'extensions': ['.rb'],
        'signatures': ['def ', 'require ', 'class ', 'module '],
        'comment': '#'
    },
    'Go': {
        'extensions': ['.go'],
        'signatures': ['package ', 'import ', 'func ', 'type '],
        'comment': '//'
    },
    'Rust': {
        'extensions': ['.rs'],
        'signatures': ['fn ', 'use ', 'struct ', 'impl ', 'pub '],
        'comment': '//'
    },
    'Swift': {
        'extensions': ['.swift'],
        'signatures': ['import ', 'func ', 'class ', 'var ', 'let '],
        'comment': '//'
    },
    'Kotlin': {
        'extensions': ['.kt', '.kts'],
        'signatures': ['fun ', 'class ', 'import ', 'val ', 'var '],
        'comment': '//'
    },
    'SQL': {
        'extensions': ['.sql'],
        'signatures': ['SELECT ', 'CREATE ', 'INSERT ', 'UPDATE ', 'DELETE '],
        'comment': '--'
    },
    'Shell': {
        'extensions': ['.sh', '.bash'],
        'signatures': ['#!/bin/bash', '#!/bin/sh', 'function ', 'export '],
        'comment': '#'
    },
    'PowerShell': {
        'extensions': ['.ps1'],
        'signatures': ['function ', 'Get-', 'Set-', '$'],
        'comment': '#'
    },
    'Markdown': {
        'extensions': ['.md', '.markdown'],
        'signatures': ['# ', '## ', '* ', '- '],
        'comment': '<!--'
    }
}

#Ігнорування шаблонів для файлових операцій
IGNORE_PATTERNS = [
    '__pycache__',
    '.git',
    '.github',
    '.gitignore',
    '.DS_Store',
    '.idea',
    '.vscode',
    '.env',
    'node_modules',
    'venv',
    'env',
    'dist',
    'build',
    'coverage',
    'logs',
    'temp',
    'tmp',
    '.log',
    '.tmp',
    '.cache',
    '.pyc',
    '.class',
    '*.backup',
    '*.swp',
    '*.bak',
    '*.swo'
]

#Дефолтні шляхи
DEFAULT_PROJECTS_PATH = os.path.expanduser('~/Projects')
DEFAULT_ORGANIZED_PATH = os.path.expanduser('~/OrganizedProjects')

#Налаштування файлів
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
DEFAULT_ENCODING = 'utf-8'
FALLBACK_ENCODINGS = ['latin-1', 'iso-8859-1', 'cp1252']

#Налаштування аналізу
MAX_PREVIEW_LINES = 50
COMPLEXITY_THRESHOLD = {
    'cyclomatic': 10,
    'cognitive': 15,
    'line_count': 200
}

#Налаштування звітів
REPORT_FORMATS = ['json', 'html', 'md', 'txt']
DEFAULT_REPORT_FORMAT = 'html'
REPORT_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

#Налаштування обробки
MAX_THREADS = os.cpu_count() or 4
BATCH_SIZE = 100

#Налаштування захисту
SENSITIVE_PATTERNS = [
    r'password\s*=\s*[\'"][^\'"]+[\'"]',
    r'api[_-]?key\s*=\s*[\'"][^\'"]+[\'"]',
    r'secret\s*=\s*[\'"][^\'"]+[\'"]',
    r'token\s*=\s*[\'"][^\'"]+[\'"]',
    r'access[_-]?key\s*=\s*[\'"][^\'"]+[\'"]',
    r'credential\s*=\s*[\'"][^\'"]+[\'"]',
    r'-----BEGIN [A-Z]+ PRIVATE KEY-----',
]

#Налаштування часу
BACKUP_RETENTION_DAYS = 30
LOG_ROTATION_SIZE = 5 * 1024 * 1024  # 5 MB

#Налаштування експорту/імпорту
EXPORT_FORMATS = ['csv', 'json', 'xlsx']
DEFAULT_EXPORT_FORMAT = 'json'

#Дефолтні розділи звіту
DEFAULT_REPORT_SECTIONS = [
    'summary',
    'file_types',
    'language_breakdown',
    'complexity_analysis',
    'potential_issues',
    'recommendations'
]

#Поріг якості коду
CODE_QUALITY_THRESHOLDS = {
    'duplication': 0.2,  # 20% duplication threshold
    'comment_ratio': 0.1,  # At least 10% comments recommended
    'test_coverage': 0.7,  # 70% minimum test coverage recommended
    'max_file_length': 500,  # Maximum recommended file length
    'max_method_length': 50,  # Maximum recommended method length
}

#Версія
VERSION = '1.0.0'


def get_config_instance(config_path=None):
    """Функція для отримання ConfigManager"""
    return ConfigManager(config_path)


#Ініціалізація конфігу по дефолту після імпорту модуля
default_config = get_config_instance()
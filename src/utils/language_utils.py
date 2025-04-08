from pathlib import Path
from typing import Optional, List, Dict
from .config import LANGUAGE_CONFIG


def detect_language(file_path: str) -> str:
    """Визначення мови програмування файлу за його розширенням

    Args:
        file_path: Шлях до файлу

    Returns:
        Назва мови програмування або 'Unknown'
    """
    ext = Path(file_path).suffix.lower()
    for lang, config in LANGUAGE_CONFIG.items():
        if ext in config['extensions']:
            return lang
    return 'Unknown'


def get_language_extensions(language: str) -> List[str]:
    """Отримання розширень файлів для певної мови

    Args:
        language: Назва мови програмування

    Returns:
        Список розширень файлів для вказаної мови
    """
    return LANGUAGE_CONFIG.get(language, {}).get('extensions', [])


def get_language_signatures(language: str) -> List[str]:
    """Отримання характерних сигнатурок для певної мови

    Args:
        language: Назва мови програмування

    Returns:
        Список характерних сигнатур для вказаної мови
    """
    return LANGUAGE_CONFIG.get(language, {}).get('signatures', [])


def get_language_comment_symbol(language: str) -> Optional[str]:
    """Отримання символів коментаря для певної мови

    Args:
        language: Назва мови програмування

    Returns:
        Символ або початок коментаря для вказаної мови
    """
    return LANGUAGE_CONFIG.get(language, {}).get('comment')


def get_all_languages() -> List[str]:
    """Отримання списків всіх підтримуваних мов програмування

    Returns:
        Список назв мов програмування
    """
    return list(LANGUAGE_CONFIG.keys())


def detect_language_from_content(content: str) -> str:
    """Визначення мови програмування за вмістом файлу

    Args:
        content: Вміст файлу

    Returns:
        Назва мови програмування або 'Unknown'
    """
    scores: Dict[str, int] = {lang: 0 for lang in LANGUAGE_CONFIG}

    #Підрахунок кількості сигнатурок для кожної мови
    for lang, config in LANGUAGE_CONFIG.items():
        for signature in config.get('signatures', []):
            count = content.count(signature)
            scores[lang] += count

    #Вибір мови з найбільшою кількістю збігів
    if any(scores.values()):
        return max(scores.items(), key=lambda x: x[1])[0]
    return 'Unknown'
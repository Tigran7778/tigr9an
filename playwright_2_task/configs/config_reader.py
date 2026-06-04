import json
import os
from typing import Optional


class ConfigReader:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(current_dir, 'config.json')
    _instance: Optional["ConfigReader"] = None
    _config: dict = {}
    _config_path: str = CONFIG_PATH

    def __new__(cls, config_path: str = CONFIG_PATH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Сохраняем путь к файлу в классе
            cls._config_path = config_path
            # Загружаем конфиг при первом создании экземпляра
            cls._instance._load_config()
        elif config_path != cls._config_path:
            # Если путь изменился, перезагружаем конфиг
            cls._config_path = config_path
            cls._instance._load_config()
        return cls._instance

    def __init__(self):
        # Инициализация происходит только один раз
        if not hasattr(self, '_initialized') or not self._initialized:
            self._initialized = True

    def _load_config(self):
        """Загружает конфигурацию из файла."""
        with open(self._config_path, 'r', encoding='utf-8') as file:
            self._config = json.load(file)

    def get_url(self):
        return self._config.get('url', '')  # Возвращает пустую строку, если ключ отсутствует

    def get_search_name(self):
        return self._config.get('search_name', '')

    def get_filters(self):
        return self._config.get('filters', {})

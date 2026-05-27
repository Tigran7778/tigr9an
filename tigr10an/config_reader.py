import json
import os
from typing import Any


class ConfigReader:
    _instance: "ConfigReader | None" = None
    _config: dict = {}

    def __new__(cls, config_path: str = "config.json") -> "ConfigReader":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load(config_path)
        return cls._instance

    def _load(self, config_path: str) -> None:
        """Загружает конфиг из JSON-файла, ищет его рядом с этим модулем."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, config_path)
        with open(full_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)

    def get(self, *keys: str, default: Any = None) -> Any:
        """Возвращает значение по цепочке ключей."""
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            if value is None:
                return default
        return value

    @classmethod
    def reset(cls) -> None:
        """Сбрасывает Singleton (используется при изолированном тестировании утилит)."""
        cls._instance = None
        cls._config = {}

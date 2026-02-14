import os
from typing import Optional
from dotenv import load_dotenv

class ConfigLoader:
    """
    Utility to load environment variables and manage secrets securely.
    """

    def __init__(self, env_path: str = ".env"):
        if os.path.exists(env_path):
            load_dotenv(env_path)
        else:
            print(f"[ConfigLoader] Warning: {env_path} not found. Using system environment variables.")

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Retrieve a configuration value by key.
        """
        return os.getenv(key, default)

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Retrieve a configuration value as an integer.
        """
        value = self.get(key)
        try:
            return int(value) if value is not None else default
        except ValueError:
            return default

    def is_production(self) -> bool:
        """
        Check if the current environment is production.
        """
        return self.get("ENV", "development").lower() == "production"

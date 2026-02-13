# config.py
"""
Configuration manager for AI Model Fetcher.
Handles loading/saving configuration from JSON file.
"""

import json
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    """
    Manages application configuration with JSON persistence.
    """
    
    DEFAULT_CONFIG = {
        "model_output_dir": "./models",
        "image_output_dir": "./images",
        "api_timeout": 30,
        "image_placeholder_count": 2
    }
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize ConfigManager.
        
        Args:
            config_file: Path to config.json file
        """
        self.config_file = Path(config_file)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self) -> None:
        """
        Load configuration from JSON file.
        If file doesn't exist, uses defaults and creates it.
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    # Merge with defaults (allows partial configs)
                    self.config.update(loaded)
                    print(f"[OK] Config geladen: {self.config_file}")
            else:
                # Create default config file
                self.save()
                print(f"[OK] Config erstellt mit Defaults: {self.config_file}")
        except Exception as e:
            print(f"[WARN] Config konnte nicht geladen werden: {e}. Verwende Defaults.")
            self.config = self.DEFAULT_CONFIG.copy()
    
    def save(self) -> None:
        """
        Save current configuration to JSON file.
        """
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"[OK] Config gespeichert: {self.config_file}")
        except Exception as e:
            print(f"[ERROR] Config konnte nicht gespeichert werden: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
        
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: New value
        """
        self.config[key] = value
    
    def get_path(self, key: str) -> Path:
        """
        Get a configuration value as Path object.
        
        Args:
            key: Configuration key for directory path
        
        Returns:
            Path object
        """
        return Path(self.get(key, "."))
    
    def set_path(self, key: str, path: Path) -> None:
        """
        Set a configuration path value.
        
        Args:
            key: Configuration key
            path: Path object
        """
        self.set(key, str(path))
    
    def to_dict(self) -> dict:
        """
        Get entire configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()

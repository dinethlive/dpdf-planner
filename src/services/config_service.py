"""
Configuration Service - Persistence for user preferences

Manages saving and loading of user preferences including last-used directories
and recent files.
"""

import os
import json
from typing import Optional, List
from pathlib import Path


class ConfigService:
    """
    Service class for managing application configuration and user preferences.
    """
    
    # Config file location in user's AppData
    CONFIG_DIR = Path(os.environ.get('APPDATA', os.path.expanduser('~'))) / 'dpdf-planner'
    CONFIG_FILE = CONFIG_DIR / 'config.json'
    
    # Default configuration
    DEFAULT_CONFIG = {
        'last_input_dir': '',
        'last_output_dir': '',
        'recent_files': [],
        'theme': 'dark',
        'max_recent_files': 5,
        'default_output_subdir': 'Extracted PDFs'
    }
    
    def __init__(self):
        self._config = self.DEFAULT_CONFIG.copy()
        self._load_config()
    
    def _ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        if not self.CONFIG_DIR.exists():
            try:
                self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass  # Fail silently - we'll just use defaults
    
    def _load_config(self):
        """Load configuration from file."""
        self._ensure_config_dir()
        
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle missing keys
                    self._config = {**self.DEFAULT_CONFIG, **loaded}
            except Exception:
                # If loading fails, use defaults
                self._config = self.DEFAULT_CONFIG.copy()
    
    def _save_config(self):
        """Save configuration to file."""
        self._ensure_config_dir()
        
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except Exception:
            pass  # Fail silently
    
    # Properties for configuration values
    
    @property
    def last_input_dir(self) -> str:
        """Get the last used input directory."""
        path = self._config.get('last_input_dir', '')
        if path and os.path.exists(path):
            return path
        return str(Path.home())
    
    @last_input_dir.setter
    def last_input_dir(self, value: str):
        """Set the last used input directory."""
        if value and os.path.exists(value):
            if os.path.isfile(value):
                value = os.path.dirname(value)
            self._config['last_input_dir'] = value
            self._save_config()
    
    @property
    def last_output_dir(self) -> str:
        """Get the last used output directory."""
        path = self._config.get('last_output_dir', '')
        if path and os.path.exists(path):
            return path
        return self.default_output_dir
    
    @last_output_dir.setter
    def last_output_dir(self, value: str):
        """Set the last used output directory."""
        if value:
            self._config['last_output_dir'] = value
            self._save_config()
    
    @property
    def default_output_dir(self) -> str:
        """Get the default output directory (Documents/Extracted PDFs)."""
        documents = Path.home() / 'Documents'
        subdir = self._config.get('default_output_subdir', 'Extracted PDFs')
        default_path = documents / subdir
        
        # Create if doesn't exist
        try:
            default_path.mkdir(parents=True, exist_ok=True)
        except Exception:
            return str(documents)
        
        return str(default_path)
    
    @property
    def recent_files(self) -> List[str]:
        """Get list of recently opened files."""
        files = self._config.get('recent_files', [])
        # Filter out files that no longer exist
        return [f for f in files if os.path.exists(f)]
    
    def add_recent_file(self, filepath: str):
        """Add a file to the recent files list."""
        if not filepath or not os.path.exists(filepath):
            return
        
        recent = self._config.get('recent_files', [])
        
        # Remove if already exists
        if filepath in recent:
            recent.remove(filepath)
        
        # Add to beginning
        recent.insert(0, filepath)
        
        # Limit to max recent files
        max_files = self._config.get('max_recent_files', 5)
        self._config['recent_files'] = recent[:max_files]
        
        self._save_config()
    
    def clear_recent_files(self):
        """Clear the recent files list."""
        self._config['recent_files'] = []
        self._save_config()
    
    @property
    def theme(self) -> str:
        """Get the current theme."""
        return self._config.get('theme', 'dark')
    
    @theme.setter
    def theme(self, value: str):
        """Set the theme."""
        if value in ('dark', 'light'):
            self._config['theme'] = value
            self._save_config()
    
    def get_output_path(self, filename: str) -> str:
        """
        Get the full output path for a filename.
        
        Args:
            filename: The output filename (with or without .pdf extension)
            
        Returns:
            Full path to the output file
        """
        if not filename.lower().endswith('.pdf'):
            filename = f"{filename}.pdf"
        
        return os.path.join(self.last_output_dir, filename)
    
    def ensure_output_dir_exists(self) -> bool:
        """
        Ensure the output directory exists.
        
        Returns:
            True if directory exists or was created, False otherwise
        """
        try:
            output_dir = self.last_output_dir
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            return True
        except Exception:
            return False

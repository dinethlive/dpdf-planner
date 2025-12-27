"""
Project Service - Manages checking/saving/loading projects
"""
import os
import json
from typing import Dict, Any, Optional

class ProjectService:
    """
    Service dealing with project persistence in [app]docs directory.
    """
    
    def __init__(self, app_docs_dir: str):
        self.app_docs_dir = app_docs_dir
        self._ensure_docs_dir()
        
    def _ensure_docs_dir(self):
        """Ensure the project directory exists."""
        if not os.path.exists(self.app_docs_dir):
            os.makedirs(self.app_docs_dir)
            
    def save_project(self, name: str, data: Dict[str, Any]) -> str:
        """
        Save project data to a JSON file.
        
        Args:
            name: Project name (used for filename)
            data: Dictionary of project data
            
        Returns:
            Path to the saved file
        """
        filename = f"{name}.json"
        filepath = os.path.join(self.app_docs_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
        return filepath
    
    def load_project(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Load project data from a JSON file.
        
        Args:
            filepath: Path to the project file
            
        Returns:
            Dictionary of project data or None if failed
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading project {filepath}: {e}")
            return None
            
    def list_projects(self) -> Dict[str, str]:
        """
        List all available projects.
        
        Returns:
            Dict mapping project names to filepaths
        """
        projects = {}
        if os.path.exists(self.app_docs_dir):
            for filename in os.listdir(self.app_docs_dir):
                if filename.endswith(".json"):
                    name = os.path.splitext(filename)[0]
                    projects[name] = os.path.join(self.app_docs_dir, filename)
        return projects

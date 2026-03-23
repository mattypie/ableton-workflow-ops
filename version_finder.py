import os
import glob
from collections import defaultdict
from datetime import datetime

class VersionFinder:
    def __init__(self, search_paths):
        self.search_paths = search_paths

    def find_projects(self):
        """
        Finds all .als files in the specified search paths, grouped by project.
        """
        project_groups = defaultdict(list)
        
        for root_path in self.search_paths:
            if not os.path.exists(root_path):
                print(f"Warning: Path {root_path} does not exist.")
                continue
                
            # Search for .als files recursively
            # We look for files ending in .als, excluding those starting with ._ (metadata files)
            als_pattern = os.path.join(root_path, "**", "*.als")
            for file_path in glob.iglob(als_pattern, recursive=True):
                filename = os.path.basename(file_path)
                if filename.startswith("._"):
                    continue
                
                # Determine Project Name
                # If inside a "Project" folder, use that folder name as the project key
                parts = file_path.split(os.sep)
                project_name = "Unknown"
                for part in reversed(parts):
                    if part.endswith(" Project"):
                        project_name = part.replace(" Project", "")
                        break
                
                if project_name == "Unknown":
                    # Fallback to the filename if not inside a Project folder
                    project_name = os.path.splitext(filename)[0]
                
                mtime = os.path.getmtime(file_path)
                project_groups[project_name].append({
                    "path": file_path,
                    "mtime": mtime,
                    "datetime": datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                })
        
        return project_groups

    def get_latest_versions(self, count=2):
        """
        Returns the latest 'count' versions for each project.
        """
        projects = self.find_projects()
        latest = {}
        
        for name, files in projects.items():
            # Sort by modification time, latest first
            sorted_files = sorted(files, key=lambda x: x['mtime'], reverse=True)
            latest[name] = sorted_files[:count]
            
        return latest

if __name__ == "__main__":
    # Paths provided by the user
    PATHS = [
        "/Volumes/T7/Daw n stuff/ableton projects 2/Projects/2023",
        "/Users/manas/Documents/AlphaCentuari/ableton auto exporter"
    ]
    
    finder = VersionFinder(PATHS)
    latest_projects = finder.get_latest_versions(count=2)
    
    print(f"Found {len(latest_projects)} unique projects.")
    
    for name, versions in list(latest_projects.items())[:5]: # Show first 5 for preview
        print(f"\nProject: {name}")
        for v in versions:
            print(f"  - {v['datetime']} | {v['path']}")

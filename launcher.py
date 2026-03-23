import os
import subprocess
import time
from version_finder import VersionFinder
from als_metadata_extractor import extract_als_metadata

class AbletonLauncher:
    def __init__(self, search_paths, output_dir=None):
        self.finder = VersionFinder(search_paths)
        self.output_dir = output_dir or "/Volumes/T7/Daw n stuff/2023 auto export"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print(f"--- [INIT] Export Location: {self.output_dir} ---")

    def cleanup_dialogs(self, stage="Generic"):
        """Clears any blocking dialogs from previous projects."""
        script_path = "/Users/manas/Documents/AlphaCentuari/ableton auto exporter/cleanup_script.applescript"
        print(f"    [LOG] Cleaning up dialogs (Stage: {stage})...")
        subprocess.run(["osascript", script_path])

    def open_als(self, als_path):
        """Opens an .als file using the macOS 'open' command."""
        print(f"    [LOG] Opening Application: {als_path}")
        subprocess.run(["open", "-a", "Ableton Live 12 Suite", als_path])

    def trigger_applescript(self, loop_start, loop_length, output_filename):
        """Calls the AppleScript to handle the export dialog."""
        script_path = "/Users/manas/Documents/AlphaCentuari/ableton auto exporter/export_script.applescript"
        output_path = os.path.join(self.output_dir, output_filename)
        
        print(f"    [LOG] Triggering AppleScript: Start={loop_start}, Length={loop_length}")
        print(f"    [LOG] File Destination: {output_path}")
        
        result = subprocess.run([
            "osascript", 
            script_path, 
            str(loop_start), 
            str(loop_length), 
            output_path
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"    [ERROR] AppleScript Failed: {result.stderr.strip()}")
            return False
        
        # AppleScript 'log' output goes to stderr
        if result.stderr:
            print(f"    [AS LOG]\n{result.stderr.strip()}")
            
        return True

    def process_projects(self, version_count=1):
        """Iterates through all projects and versions with tiered loading."""
        latest_projects = self.finder.get_latest_versions(count=version_count)
        total = len(latest_projects)
        print(f"--- [START] Found {total} projects to process ---")
        
        count = 0
        for project_name, versions in latest_projects.items():
            if project_name != "1 interlude":
                continue
            
            count += 1
            for version in versions:
                als_path = version['path']
                print(f"\n[TARGET: {project_name}] >>> Processing...")
                
                # 1. Get Metadata
                metadata = extract_als_metadata(als_path)
                if not metadata:
                    print(f"    [SKIP] Could not extract metadata from {als_path}")
                    continue
                
                # 2. Open Ableton
                self.open_als(als_path)
                
                # 2.5 Handle the initial "Save changes" / "Stop audio" prompts
                # We wait a bit more for System Events to register the 'Live' process
                time.sleep(4) 
                self.cleanup_dialogs("Initial Launch")
                
                # 3. Tiered loading wait
                wait_tiers = [5, 10, 20] # Total cumulative: 5, 15, 35
                success = False
                
                for i, wait_time in enumerate(wait_tiers):
                    print(f"    [WAIT] Tier {i+1}: Waiting {wait_time}s for project load...")
                    time.sleep(wait_time)
                    
                    # 4. Attempt Export
                    output_filename = f"{project_name}_{int(time.time())}.wav"
                    if self.trigger_applescript(metadata['start_str'], metadata['length_str'], output_filename):
                        print(f"    [SUCCESS] Export triggered for {project_name}")
                        success = True
                        break
                    else:
                        if i < len(wait_tiers) - 1:
                            print(f"    [RETRY] Export dialog failed. Waiting more time (Tier {i+2})...")
                        else:
                            print(f"    [FAIL] Max tiers reached. Skipping {project_name}.")
                
                if success:
                    # Brief wait for export to initialize/block before moving to next project
                    time.sleep(5) 

if __name__ == "__main__":
    PATHS = [
        "/Volumes/T7/Daw n stuff/ableton projects 2/Projects/2023",
        "/Users/manas/Documents/AlphaCentuari/ableton auto exporter"
    ]
    
    launcher = AbletonLauncher(PATHS)
    launcher.process_projects(version_count=1)

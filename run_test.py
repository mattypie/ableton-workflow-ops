from launcher import AbletonLauncher

PATHS = [
    "/Volumes/T7/Daw n stuff/ableton projects 2/Projects/2023",
    "/Users/manas/Documents/AlphaCentuari/ableton auto exporter"
]

# Initialize launcher
launcher = AbletonLauncher(PATHS, mode="realtime")

# Test export for a single project
# Note: This will open Ableton. Ensure the Max for Live device is in the project!
launcher.test_single_project("1 interlude")

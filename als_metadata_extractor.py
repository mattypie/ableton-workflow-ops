import gzip
import xml.etree.ElementTree as ET
import os

def extract_als_metadata(als_path):
    """
    Extracts LoopStart and LoopLength from an Ableton .als file.
    """
    if not os.path.exists(als_path):
        return None
        
    try:
        with gzip.open(als_path, 'rb') as f:
            xml_content = f.read()
            
        root = ET.fromstring(xml_content)
        
        # Ableton XML structure:
        # LiveSet -> Transport -> LoopStart / LoopLength
        # Actually, it's often in LiveSet -> Song -> Transport
        
        transport = root.find(".//Transport")
        if transport is not None:
            loop_on = transport.find("LoopOn")
            loop_start = transport.find("LoopStart")
            loop_length = transport.find("LoopLength")
            
            raw_start = float(loop_start.attrib.get('Value')) if loop_start is not None else 0
            raw_length = float(loop_length.attrib.get('Value')) if loop_length is not None else 0
            
            # Simple conversion assuming 4/4 time signature
            # Bars = beats // 4 + 1
            # Beats = (beats % 4) + 1
            start_bar = int(raw_start // 4) + 1
            start_beat = int(raw_start % 4) + 1
            
            length_bars = int(raw_length // 4)
            length_beats = int(raw_length % 4)
            
            return {
                "loop_on": loop_on.attrib.get('Value') if loop_on is not None else None,
                "start": raw_start,
                "length": raw_length,
                "start_str": f"{start_bar}.{start_beat}.1",
                "length_str": f"{length_bars}.{length_beats}.0"
            }
    except Exception as e:
        print(f"Error parsing XML for {als_path}: {e}")
        return None

if __name__ == "__main__":
    test_file = "/Volumes/T7/Daw n stuff/ableton projects 2/Projects/2023/1 interlude Project/1 interlude.als"
    metadata = extract_als_metadata(test_file)
    if metadata:
        print(f"Metadata for: {os.path.basename(test_file)}")
        print(f"  Loop On: {metadata['loop_on']}")
        print(f"  Start: {metadata['start']}")
        print(f"  Length: {metadata['length']}")
    else:
        print("Failed to extract metadata.")

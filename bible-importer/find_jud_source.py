import xml.etree.ElementTree as ET
import os

OSIS_NS = "http://www.bibletechnologies.net/2003/OSIS/namespace"

directory = "data/morphhb/wlc"

# Procura por qualquer verse com osisID contendo JUD
for filename in os.listdir(directory):
    if not filename.endswith(".xml"):
        continue
    
    filepath = os.path.join(directory, filename)
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        found_jud = False
        for verse_elem in root.iter(f"{{{OSIS_NS}}}verse"):
            osisID = verse_elem.get("osisID", "")
            if "JUD" in osisID or osisID.startswith("Jud"):
                if not found_jud:
                    print(f"\n{filename}:")
                    found_jud = True
                print(f"  osisID: {osisID}")
                if found_jud and osisID.count(".") >= 2:
                    break
    except Exception as e:
        pass

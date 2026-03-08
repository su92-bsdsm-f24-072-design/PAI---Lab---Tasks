import sys
import os

# Add project folder to path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.detection import detect_animals
from utils.map_alert import plot_on_map

print("Imports working!")

# Test functions
print(detect_animals("dummy.jpg"))
print(plot_on_map([]))
# utils/map_alert.py
import folium
import os

def plot_on_map(detections):
    """
    Create an interactive map with detected animals.
    Returns the path to HTML file.
    """
    # Create a map centered at some location (example: farm coordinates)
    map_center = [30.3753, 69.3451]  # Pakistan center, change as needed
    m = folium.Map(location=map_center, zoom_start=6)

    for d in detections:
        folium.Marker(
            location=[map_center[0] + d['y']*0.0001, map_center[1] + d['x']*0.0001],  # small shift for demo
            popup=d['animal']
        ).add_to(m)

    # Save map HTML inside static folder
    map_file = os.path.join('static', 'map.html')
    m.save(map_file)
    return 'static/map.html'
import json
import urllib.parse
import requests
import time
import os

API_KEY = 'AIzaSyB9_MF2J2Lkb2WhL2-fwwRkfsobBJ0Clps'

def geocode(address):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(address)}&key={API_KEY}'
    try:
        res = requests.get(url, timeout=10).json()
        if res.get('status') == 'OK' and res.get('results'):
            loc = res['results'][0]['geometry']['location']
            return loc['lat'], loc['lng'], res['results'][0]['formatted_address']
    except Exception as e:
        print(f'  Geocode error: {e}')
    return None, None, address

locations_data = [
    {"name": "Thomas Wolfe Memorial house (facing the hotel)", "address": "52 N Market St, Asheville, NC 28801"},
    {"name": "Urban trail marker: Thomas Wolfe's neighborhood (1900-1924)", "address": "52 N Market St, Asheville, NC 28801"},
    {"name": "Chicken Alley (1930-1950)", "address": "8 Chicken Aly, Asheville, NC 28801"},
    {"name": "Asheville Showcase (1960s)", "address": "57-59 Broadway St, Asheville, NC 28801"},
    {"name": "Moogseum", "address": "56 Broadway St, Asheville, NC 28801"},
    {"name": "Mellow Mushroom", "address": "50 Broadway St, Asheville, NC 28801"},
    {"name": "Blomberg Annex to Asheville Community Theatre (ACT) (1923)", "address": "35 E Walnut St, Asheville, NC 28801"},
    {"name": "Asheville Community Theatre (ACT) (1940-PRESENT)", "address": "35 E Walnut St, Asheville, NC 28801"},
    {"name": "Finklesteins Pawn Shop (1903-PRESENT)", "address": "21 Broadway St, Asheville, NC 28801"},
    {"name": "Black Mountain College Tribute Wall (1933-1957)", "address": "5 W Walnut St, Asheville, NC 28801"},
    {"name": "Vanderbilt Shirt Factory (1950s)", "address": "65 W Walnut St, Asheville, NC 28801"},
    {"name": "Tops for Shoes (1950s-PRESENT)", "address": "27 N Lexington Ave, Asheville, NC 28801"},
    {"name": "Coleman Zageir and the Man's Store (1922-1962)", "address": "22 Patton Ave, Asheville, NC 28801"},
    {"name": "S and W Cafeteria (1929-1974)", "address": "56 Patton Ave, Asheville, NC 28801"},
    {"name": "Flatiron building", "address": "20 Battery Park Ave, Asheville, NC 28801"},
    {"name": "Pollock Crest", "address": "39 Patton Ave, Asheville, NC 28801"},
    {"name": "Earth Guild", "address": "33 Haywood St, Asheville, NC 28801"},
    {"name": "Urban Trail Marker to shoppers (1880-1990)", "address": "55 Haywood St, Asheville, NC 28801"},
    {"name": "Fine Arts theater (optional) (1947-1960s)", "address": "36 Biltmore Ave, Asheville, NC 28801"}
]

markers = []
for loc in locations_data:
    print(f"Geocoding {loc['name']}...")
    lat, lng, fmt = geocode(loc['address'])
    time.sleep(0.15)
    
    markers.append({
        "name": loc['name'],
        "address": fmt if fmt else loc['address'],
        "lat": lat,
        "lng": lng
    })

markers_json = json.dumps(markers, indent=4)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asheville Landmarks Map</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>
    <script src="https://unpkg.com/@googlemaps/markerclusterer/dist/index.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        #map {{
            height: 100vh;
            width: 100vw;
        }}
        .info-window {{
            padding: 10px;
            max-width: 300px;
        }}
        .info-window h3 {{
            margin: 0 0 10px 0;
            font-size: 16px;
            color: #333;
        }}
        .info-window p {{
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #666;
        }}
        .info-window a {{
            color: #1a73e8;
            text-decoration: none;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div id="map"></div>

    <script>
        const locations = {markers_json};

        function initMap() {{
            const map = new google.maps.Map(document.getElementById("map"), {{
                zoom: 15,
                center: {{ lat: 35.5951, lng: -82.5515 }}, // Centered on Asheville
                mapTypeId: "roadmap",
            }});

            const infoWindow = new google.maps.InfoWindow();
            const markers = locations.map((loc) => {{
                if (loc.lat && loc.lng) {{
                    const marker = new google.maps.Marker({{
                        position: {{ lat: loc.lat, lng: loc.lng }},
                        title: loc.name,
                    }});

                    marker.addListener("click", () => {{
                        const content = `
                            <div class="info-window">
                                <h3>${{loc.name}}</h3>
                                <p>${{loc.address}}</p>
                                <a href="https://www.google.com/maps/search/?api=1&query=${{loc.lat}},${{loc.lng}}" target="_blank">View on Google Maps</a>
                            </div>
                        `;
                        infoWindow.setContent(content);
                        infoWindow.open(map, marker);
                    }});

                    return marker;
                }}
                return null;
            }}).filter(m => m !== null);

            new markerClusterer.MarkerClusterer({{ map, markers }});
        }}
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key={API_KEY}&callback=initMap" async defer></script>
</body>
</html>
"""

with open('asheville.html', 'w') as f:
    f.write(html_content)

print(f"\\nSuccessfully generated asheville.html with {len(markers)} markers.")

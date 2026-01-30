import osmium

class PincodeHandler(osmium.SimpleHandler):
    def __init__(self, target_pincode):
        super(PincodeHandler, self).__init__()
        self.target_pincode = str(target_pincode)
        self.cities = set()

    def _check_tags(self, tags):
        """Helper to check tags on any OSM object (node, way, or relation)."""
        postcode = tags.get('addr:postcode')
        city = tags.get('addr:city')
        
        if postcode == self.target_pincode and city:
            # We add to a set to handle duplicates automatically
            self.cities.add(city)

    def node(self, n):
        self._check_tags(n.tags)

    def way(self, w):
        self._check_tags(w.tags)

    def relation(self, r):
        self._check_tags(r.tags)

def get_city_from_pincode(pbf_file_path, pincode):
    # Initialize and apply the handler
    handler = PincodeHandler(pincode)
    handler.apply_file(pbf_file_path)

    # Logic to store the result in a single variable
    if handler.cities:
        # Use next(iter()) to pick one, then .title() to fix 'ujjain' -> 'Ujjain'
        return next(iter(handler.cities)).title()
    return None

# --- MAIN EXECUTION ---
# Path to your local OSM data file from Geofabrik or similar
osm_file = "/home/mradul/Desktop/Ekadyu/AI-Transliteration/osm-data/central-zone-260126.osm.pbf" 
target_pin = "456001"

# The final result is stored in this variable
city_name = get_city_from_pincode(osm_file, target_pin)

# Verification
if city_name:
    print(f"Success! The city name is stored in the variable: {city_name}")
else:
    print("City not found for this pincode in the provided file.")


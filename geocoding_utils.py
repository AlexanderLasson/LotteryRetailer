import googlemaps

def get_county_from_address(address, gmaps):
    # Use geocoding to get detailed address components including county
    geocode_result = gmaps.geocode(address)

    # Extract county from address components
    for component in geocode_result[0]['address_components']:
        if 'administrative_area_level_2' in component['types']:
            return component['long_name']

    return 'N/A'
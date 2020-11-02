

def coordinates_from_region_code(region_code: str) -> [float, float]:
    lat = None
    long = None
    if region_code == "RU":
        lat, long = 55.7558, 37.6173
    return lat, long

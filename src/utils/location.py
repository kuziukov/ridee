

def coordinates_from_region_code(region_code) -> [float, float]:
    lat = 0
    long = 0
    if region_code == "RU":
        lat, long = 55.7558, 37.6173
    return lat, long
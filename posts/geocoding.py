from functools import lru_cache

from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim


@lru_cache(maxsize=1)
def _get_geocoder():
    return Nominatim(user_agent="social-network-backend")


def geocode_location(query):
    if not query:
        return None, None
    try:
        location = _get_geocoder().geocode(query, timeout=5)
    except (GeocoderServiceError, OSError, ValueError):
        return None, None
    if not location:
        return None, None
    return location.latitude, location.longitude


def reverse_location(latitude, longitude):
    if latitude is None or longitude is None:
        return None
    try:
        location = _get_geocoder().reverse(
            f"{latitude}, {longitude}",
            timeout=5,
            language="ru",
        )
    except (GeocoderServiceError, OSError, ValueError):
        return None
    if not location:
        return None
    return location.address

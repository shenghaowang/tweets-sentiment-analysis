from typing import Tuple

import stanza
from geopy.geocoders import Nominatim

stanza.download("en")
geolocator = Nominatim(user_agent="geoapi")

# Load the English NLP pipeline with Named Entity Recognition (NER)
nlp = stanza.Pipeline(lang="en", processors="tokenize,ner")


def identify_location(text: str) -> str:
    """Identify valid location from tweet

    Parameters
    ----------
    text : str
        tweet message

    Returns
    -------
    str
        location entity identified
    """
    doc = nlp(text)
    locations = [ent.text for ent in doc.entities if ent.type == "GPE"]

    return locations[0] if locations else None


def get_geocode(location: str) -> Tuple[float, float]:
    """Obtain geo-coordinates from location name

    Parameters
    ----------
    location : str
        location name

    Returns
    -------
    Tuple[float, float]
        latitude and logitude
    """
    location = geolocator.geocode(location)
    if location:
        return location.latitude, location.longitude

    return None, None

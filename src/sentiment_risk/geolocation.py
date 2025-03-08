import stanza

stanza.download("en")

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

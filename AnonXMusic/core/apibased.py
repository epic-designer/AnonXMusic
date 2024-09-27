import lyricsgenius
import config
from ..logging import LOGGER

# API based clients
def APIbased():
    if config.GENIUS_API_TOKEN:
        LOGGER(__name__).info("Found Genius API token, initializing client")
        genius_lyrics = lyricsgenius.Genius(
            config.GENIUS_API_TOKEN,
            skip_non_songs=True,
            excluded_terms=["(Remix)", "(Live)"],
            remove_section_headers=True,
        )
        is_genius_lyrics = True

        genius_lyrics.verbose = False
        LOGGER(__name__).info("Client setup complete")
    else:
        LOGGER(__name__).error("Genius API token not found, lyrics command will not work")
        is_genius_lyrics = False
        genius_lyrics = None

    is_audd = False
    Audd = None
    if config.AuDD_API:
        is_audd = True
        Audd = config.AuDD_API
        LOGGER(__name__).info("Found Audd API")

    is_rmbg = False
    RMBG = None
    if config.RMBG_API:
        is_rmbg = True
        RMBG = config.RMBG_API

    return is_genius_lyrics, genius_lyrics, is_audd, Audd, is_rmbg, RMBG

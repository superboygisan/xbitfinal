from .extras import *
from .help import *
# play.py se direct functions nikalne ke bajay hum sirf 'Inline' class ko import karenge
from .play import Inline
from .queue import *
from .settings import *
from .speed import *
from .start import *

# Yahan humne class ko mention karke uska object bana diya
buttons = Inline()

# SAFE MAPPING: getattr() use karne se agar attribute nahi mila toh bot CRASH nahi hoga!
track_markup = getattr(buttons, "track_markup", None)
stream_markup = getattr(buttons, "track_markup", None)
playlist_markup = getattr(buttons, "playlist_markup", None)
livestream_markup = getattr(buttons, "livestream_markup", None)
slider_markup = getattr(buttons, "slider_markup", None)

# Timer wale attribute ke liye backup checks
if hasattr(buttons, "track_markup_timer"):
    stream_markup_timer = buttons.track_markup_timer
elif hasattr(buttons, "stream_markup_timer"):
    stream_markup_timer = buttons.stream_markup_timer
else:
    # Agar dono nahi mile, toh normal track_markup use kar lega par crash nahi hoga
    stream_markup_timer = track_markup

__all__ = [
    "track_markup",
    "stream_markup",
    "stream_markup_timer",
    "playlist_markup",
    "livestream_markup",
    "slider_markup",
]
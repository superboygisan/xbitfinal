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

# Ab us class ke andar ke saare functions ko explicitly mention kar dete hain
track_markup = buttons.track_markup
stream_markup = buttons.track_markup
stream_markup_timer = buttons.stream_markup_timer
playlist_markup = buttons.playlist_markup
livestream_markup = buttons.livestream_markup
slider_markup = buttons.slider_markup

_all_ = [
    "track_markup",
    "stream_markup",
    "stream_markup_timer",
    "playlist_markup",
    "livestream_markup",
    "slider_markup",
]
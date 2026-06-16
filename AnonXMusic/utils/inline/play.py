import math
from pyrogram import enums, types

class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

        self.styles = {
            "default": enums.ButtonStyle.DEFAULT,
            "primary": enums.ButtonStyle.PRIMARY,
            "success": enums.ButtonStyle.SUCCESS,
            "danger": enums.ButtonStyle.DANGER,
        }

    def _button(self, text: str, category: str = "default", **kwargs):
        return self.ikb(
            text=text,
            style=self.styles.get(category, enums.ButtonStyle.DEFAULT),
            **kwargs,
        )

    # MAIN CONTROL HUB
    def track_markup(self, _, chat_id: int, status: str = None, timer_row: list = None, remove: bool = False):
        keyboard = []

        # Abstract Graphic Progress Button sabse upar rahega
        if timer_row:
            keyboard.append(timer_row)
        elif status:
            keyboard.append([self._button(text=status, category="default", callback_data="noop")])

        # MAIN CONTROLS ROW (Sleek Compact Layout - No text on buttons)
        if not remove:
            keyboard.append(
                [
                    self._button(
                        text="▶️",
                        category="success",
                        callback_data=f"ADMIN Resume|{chat_id}",
                    ),
                    self._button(
                        text="⏮️",
                        category="primary",
                        callback_data=f"ADMIN Replay|{chat_id}",
                    ),
                    self._button(
                        text="⏸️",
                        category="primary",
                        callback_data=f"ADMIN Pause|{chat_id}",
                    ),
                    self._button(
                        text="⏭️",
                        category="primary",
                        callback_data=f"ADMIN Skip|{chat_id}",
                    ),
                    self._button(
                        text="⏹️",
                        category="danger",
                        callback_data=f"ADMIN Stop|{chat_id}",
                    ),
                ]
            )

        # Pyrogram InlineKeyboardMarkup structure returns directly here
        return self.ikm(keyboard) if hasattr(self, "ikm") else keyboard

    # INTERACTIVE LOADING BAR WITH HALF MOON POINTER
    def stream_markup_timer(self, _, chat_id: int, played: str, duration: str):
        try:
            p_min, p_sec = map(int, played.split(":"))
            d_min, d_sec = map(int, duration.split(":"))

            played_seconds = (p_min * 60) + p_sec
            total_seconds = (d_min * 60) + d_sec

            percentage = (played_seconds / total_seconds) * 100 if total_seconds > 0 else 0
        except:
            percentage = 0

        # Total 12 steps ka premium loading grid
        total_steps = 12

        active_pos = math.floor((percentage / 100) * total_steps)
        if active_pos >= total_steps:
            active_pos = total_steps - 1

        bar_text = ""
        for i in range(total_steps):
            if i < active_pos:
                # Loaded Block (Filled area)
                bar_text += "▰" 
            elif i == active_pos:
                # Half Moon Moving Pointer Knob
                bar_text += "🌓"
            else:
                # Empty Block (Buffer area)
                bar_text += "▱"

        # Ultra Realistic Professional Loading Layout Look
        full_graphic_bar = f"⏱️ {played} [{bar_text}] {duration}"

        # End phase par button automatic Red/Danger ho jayega
        button_color = "danger" if percentage >= 85 else "success"
        timer_row = [self._button(text=full_graphic_bar, category=button_color, callback_data="noop")]

        return self.track_markup(_, chat_id, timer_row=timer_row)

    # ALL RECOVERY BACKUPS TO PREVENT SYSTEM CRASH
    def playlist_markup(self, _, chat_id: int): return self.track_markup(_, chat_id)
    def livestream_markup(self, _, chat_id: int): return self.track_markup(_, chat_id)
    def slider_markup(self, _, chat_id: int): return self.track_markup(_, chat_id)
    def queue_markup(self, chat_id: int, text: str, playing: bool = False):
        action = "pause" if playing else "resume"
        return self.ikm([[self._button(text=text, category="success" if playing else "danger", callback_data=f"ADMIN {action.capitalize()}|{chat_id}")]])
    def play_queued(self, chat_id: int, item_id: str, text: str):
        return self.ikm([[self._button(text=text, category="success", callback_data=f"ADMIN Resume|{chat_id}")]])
    def yt_key(self, link: str):
        return self.ikm([[self._button(text="📋 Copy Link", category="primary", copy_text=link), self._button(text="🎬 YouTube", category="danger", url=link)]])

buttons = Inline()

# MAPPING ALL VARIABLES FOR FULL PLUGIN COMPATIBILITY
controls = buttons.track_markup
track_markup = buttons.track_markup
stream_markup = buttons.track_markup
stream_markup_timer = buttons.stream_markup_timer
playlist_markup = buttons.playlist_markup
livestream_markup = buttons.livestream_markup
slider_markup = buttons.slider_markup
queue_markup = buttons.queue_markup
play_queued = buttons.play_queued
yt_key = buttons.yt_key
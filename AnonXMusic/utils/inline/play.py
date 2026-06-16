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

        if timer_row:
            keyboard.append(timer_row)
        elif status:
            keyboard.append([self._button(text=status, category="default", callback_data="noop")])
        else:
            # Clean initial loading bar style
            keyboard.append([self._button(text="⏳ 𝟬values𝟬 ❖ ▬▱▱▱▱▱▱▱▱▱ ❖ 𝟬𝟬:𝟬𝟬", category="success", callback_data="noop")])

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

        return keyboard

    # INTERACTIVE PROGRESS LOADING LOOP
    def stream_markup_timer(self, _, chat_id: int, played: str = "00:00", duration: str = "00:00"):
        def to_script_font(time_str):
            font_map = {'0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵', ':': ':'}
            return "".join(font_map.get(c, c) for c in time_str)

        try:
            p_min, p_sec = map(int, str(played).split(":"))
            d_min, d_sec = map(int, str(duration).split(":"))

            played_seconds = (p_min * 60) + p_sec
            total_seconds = (d_min * 60) + d_sec

            percentage = (played_seconds / total_seconds) * 100 if total_seconds > 0 else 0
        except:
            percentage = 0

        # Sleek Loading Matrix
        total_steps = 10
        active_pos = math.floor((percentage / 100) * total_steps)
        if active_pos >= total_steps:
            active_pos = total_steps - 1

        bar_text = ""
        for i in range(total_steps):
            if i < active_pos:
                bar_text += "■"  # Completed loading blocks
            elif i == active_pos:
                bar_text += "▶"  # Head runner loader pointer
            else:
                bar_text += "▱"  # Empty path remaining

        played_font = to_script_font(str(played))
        duration_font = to_script_font(str(duration))

        # Balanced loading UI format string
        full_graphic_bar = f"⏳ {played_font} ❖ {bar_text} ❖ {duration_font}"

        button_color = "danger" if percentage >= 85 else "success"
        timer_row = [self._button(text=full_graphic_bar, category=button_color, callback_data="noop")]

        return self.ikm(self.track_markup(_, chat_id, timer_row=timer_row))

    def stream_markup_fallback(self, _, chat_id: int):
        return self.stream_markup_timer(_, chat_id, played="00:00", duration="00:00")

    def playlist_markup(self, _, chat_id: int): return self.ikm(self.track_markup(_, chat_id))
    def livestream_markup(self, _, chat_id: int): return self.ikm(self.track_markup(_, chat_id))
    def slider_markup(self, _, chat_id: int): return self.ikm(self.track_markup(_, chat_id))
    
    def queue_markup(self, chat_id: int, text: str, playing: bool = False):
        action = "pause" if playing else "resume"
        return self.ikm([[self._button(text=text, category="success" if playing else "danger", callback_data=f"ADMIN {action.capitalize()}|{chat_id}")]])
        
    def play_queued(self, chat_id: int, item_id: str, text: str):
        return self.ikm([[self._button(text=text, category="success", callback_data=f"ADMIN Resume|{chat_id}")]])
        
    def yt_key(self, link: str):
        return self.ikm([[self._button(text="📋 Copy Link", category="primary", copy_text=link), self._button(text="🎬 YouTube", category="danger", url=link)]])

buttons = Inline()

# HOOK OVERRIDES MAPPED
controls = buttons.track_markup
track_markup = buttons.track_markup
stream_markup = buttons.stream_markup_fallback  
stream_markup_timer = buttons.stream_markup_timer
playlist_markup = buttons.playlist_markup
livestream_markup = buttons.livestream_markup
slider_markup = buttons.slider_markup
queue_markup = buttons.queue_markup
play_queued = buttons.play_queued
yt_key = buttons.yt_key
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
        if "url" in kwargs and kwargs["url"]:
            url_str = str(kwargs["url"]).strip()
            if not (url_str.startswith("http://") or url_str.startswith("https://")):
                kwargs["url"] = f"https://t.me/Telegram"
        return self.ikb(
            text=text,
            style=self.styles.get(category, enums.ButtonStyle.DEFAULT),
            **kwargs,
        )

    def track_markup(self, _, chat_id: int, status: str = None, timer_row: list = None, remove: bool = False):
        keyboard = []

        if timer_row:
            keyboard.append(timer_row)
        elif status:
            keyboard.append([self._button(text=status, category="default", callback_data="noop")])
        else:
            keyboard.append([self._button(text="⏳ 00:00 ▬▬▬▬▬▬▬▬▬▬ 00:00", category="success", callback_data="noop")])

        if not remove:
            keyboard.append(
                [
                    self._button(text="▶️", category="success", callback_data=f"ADMIN Resume|{chat_id}"),
                    self._button(text="⏮️", category="primary", callback_data=f"ADMIN Replay|{chat_id}"),
                    self._button(text="⏸️", category="primary", callback_data=f"ADMIN Pause|{chat_id}"),
                    self._button(text="⏭️", category="primary", callback_data=f"ADMIN Skip|{chat_id}"),
                    self._button(text="⏹️", category="danger", callback_data=f"ADMIN Stop|{chat_id}"),
                ]
            )
        return keyboard

    def stream_markup_timer(self, _, chat_id: int, played: str = "00:00", duration: str = "00:00"):
        try:
            p_min, p_sec = map(int, str(played).split(":"))
            d_min, d_sec = map(int, str(duration).split(":"))
            played_seconds = (p_min * 60) + p_sec
            total_seconds = (d_min * 60) + d_sec
            percentage = (played_seconds / total_seconds) * 100 if total_seconds > 0 else 0
        except:
            percentage = 0

        # Standard clean slider layout bar (10 steps)
        total_steps = 10
        active_pos = math.floor((percentage / 100) * total_steps)
        if active_pos >= total_steps:
            active_pos = total_steps - 1

        bar_text = ""
        for i in range(total_steps):
            if i == active_pos:
                bar_text += "🔘" # Active tracker point
            else:
                bar_text += "▬"

        # CHANGED: Ab bilkul plain standard stable numbers use honge (No fancy fonts to avoid rendering crash)
        full_graphic_bar = f"⏳ {played} {bar_text} {duration}"

        button_color = "danger" if percentage >= 85 else "success"
        timer_row = [self._button(text=full_graphic_bar, category=button_color, callback_data="noop")]

        raw_layout = self.track_markup(_, chat_id, timer_row=timer_row)
        return self.ikm(raw_layout)

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
        clean_link = str(link).strip() if link else "https://youtube.com"
        if not (clean_link.startswith("http://") or clean_link.startswith("https://")):
            clean_link = f"https://{clean_link}"
        return self.ikm([[self._button(text="📋 Copy Link", category="primary", copy_text=clean_link), self._button(text="🎬 YouTube", category="danger", url=clean_link)]])

buttons = Inline()

controls = lambda *args, **kwargs: buttons.ikm(buttons.track_markup(*args, **kwargs))
track_markup = lambda *args, **kwargs: buttons.ikm(buttons.track_markup(*args, **kwargs))
stream_markup = lambda _, chat_id: buttons.stream_markup_fallback(_, chat_id)
stream_markup_timer = lambda _, chat_id, played="00:00", duration="00:00": buttons.stream_markup_timer(_, chat_id, played, duration)
playlist_markup = lambda _, chat_id: buttons.playlist_markup(_, chat_id)
livestream_markup = lambda _, chat_id: buttons.livestream_markup(_, chat_id)
slider_markup = lambda _, chat_id: buttons.slider_markup(_, chat_id)
queue_markup = buttons.queue_markup
play_queued = buttons.play_queued
yt_key = buttons.yt_key
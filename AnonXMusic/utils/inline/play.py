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

    # MAIN PLAYER CONTROLS & STREAM MARKUP (Dono ka kaam yahi karega)
    def track_markup(self, _, chat_id: int, status: str = None, timer: str = None, remove: bool = False):
        keyboard = []

        if status or timer:
            keyboard.append(
                [
                    self._button(
                        text=status or timer,
                        category="default",
                        callback_data="noop",
                    )
                ]
            )

        if not remove:
            keyboard.append(
                [
                    self._button(
                        text="⏮️ Replay",
                        category="primary",
                        callback_data=f"ADMIN Replay|{chat_id}",
                    ),
                    self._button(
                        text="⏸️ Pause",
                        category="primary",
                        callback_data=f"ADMIN Pause|{chat_id}",
                    ),
                    self._button(
                        text="▶️ Resume",
                        category="success",
                        callback_data=f"ADMIN Resume|{chat_id}",
                    ),
                ]
            )
            keyboard.append(
                [
                    self._button(
                        text="⏭️ Skip",
                        category="primary",
                        callback_data=f"ADMIN Skip|{chat_id}",
                    ),
                    self._button(
                        text="⏹️ Stop",
                        category="danger",
                        callback_data=f"ADMIN Stop|{chat_id}",
                    ),
                ]
            )

        # Agar Pyrogram list mangta hai toh seedhe list return karega
        return keyboard

    # STREAM MARKUP TIMER (Jo callback.py ko loop ke liye chahiye)
    def stream_markup_timer(self, _, chat_id: int, played: str, duration: str):
        # Timer strip upar dikhane ke liye
        timer_text = f"{played} ▬▬▬▬▬▬▬▬▬ {duration}"
        return self.track_markup(_, chat_id, timer=timer_text)

    # BACKUP FOR OTHER MARKUPS TO PREVENT CRASH
    def playlist_markup(self, _, chat_id: int):
        return self.track_markup(_, chat_id)

    def livestream_markup(self, _, chat_id: int):
        return self.track_markup(_, chat_id)

    def slider_markup(self, _, chat_id: int):
        return self.track_markup(_, chat_id)

    # QUEUE BUTTON
    def queue_markup(self, chat_id: int, text: str, playing: bool = False):
        action = "pause" if playing else "resume"
        keyboard = [
            [
                self._button(
                    text=text,
                    category="success" if playing else "danger",
                    callback_data=f"ADMIN {action.capitalize()}|{chat_id}",
                )
            ]
        ]
        return self.ikm(keyboard)

    # FORCE PLAY BUTTON
    def play_queued(self, chat_id: int, item_id: str, text: str):
        keyboard = [
            [
                self._button(
                    text=text,
                    category="success",
                    callback_data=f"ADMIN Resume|{chat_id}",
                )
            ]
        ]
        return self.ikm(keyboard)

    # YOUTUBE BUTTONS
    def yt_key(self, link: str):
        keyboard = [
            [
                self._button(
                    text="📋 Copy Link",
                    category="primary",
                    copy_text=link,
                ),
                self._button(
                    text="🎬 YouTube",
                    category="danger",
                    url=link,
                ),
            ]
        ]
        return self.ikm(keyboard)


buttons = Inline()

# MAPPING FOR BOTH COMPATIBILITY AND STYLING
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
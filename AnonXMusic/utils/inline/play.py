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

    # MAIN PLAYER CONTROLS
    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
    ):

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
                        text="⏮️",
                        category="primary",
                        callback_data=f"controls replay {chat_id}",
                    ),
                    self._button(
                        text="⏸️",
                        category="primary",
                        callback_data=f"controls pause {chat_id}",
                    ),
                    self._button(
                        text="▶️",
                        category="success",
                        callback_data=f"controls resume {chat_id}",
                    ),
                    self._button(
                        text="⏭️",
                        category="primary",
                        callback_data=f"controls skip {chat_id}",
                    ),
                    self._button(
                        text="⏹️",
                        category="danger",
                        callback_data=f"controls stop {chat_id}",
                    ),
                ]
            )

        return self.ikm(keyboard)

    # TRACK BUTTON
    def track_markup(
        self,
        videoid: str,
        user_id: int = None,
    ):

        keyboard = [
            [
                self._button(
                    text="📺 YouTube",
                    category="primary",
                    url=f"https://youtube.com/watch?v={videoid}",
                )
            ]
        ]

        return self.ikm(keyboard)

    # QUEUE BUTTON
    def queue_markup(
        self,
        chat_id: int,
        text: str,
        playing: bool = False,
    ):

        action = "pause" if playing else "resume"

        keyboard = [
            [
                self._button(
                    text=text,
                    category="success" if playing else "danger",
                    callback_data=f"controls {action} {chat_id} q",
                )
            ]
        ]

        return self.ikm(keyboard)

    # FORCE PLAY BUTTON
    def play_queued(
        self,
        chat_id: int,
        item_id: str,
        text: str,
    ):

        keyboard = [
            [
                self._button(
                    text=text,
                    category="success",
                    callback_data=f"controls force {chat_id} {item_id}",
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

controls = buttons.controls
track_markup = buttons.track_markup
queue_markup = buttons.queue_markup
play_queued = buttons.play_queued
yt_key = buttons.yt_key
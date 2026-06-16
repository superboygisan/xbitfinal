```python id="7srqcf"
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


inline = Inline()
```

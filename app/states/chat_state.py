import reflex as rx
import asyncio
from typing import TypedDict, Literal


class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class Conversation(TypedDict):
    id: int
    name: str
    messages: list[Message]


initial_conversations: list[Conversation] = [
    {
        "id": 1,
        "name": "Getting Started",
        "messages": [
            {"role": "assistant", "content": "Hello! How can I help you today?"},
            {"role": "user", "content": "I'd like to learn more about Reflex."},
            {
                "role": "assistant",
                "content": "Great! Reflex is a full-stack Python framework that makes it easy to build and deploy web apps. What would you like to know?",
            },
        ],
    },
    {
        "id": 2,
        "name": "UI/UX Design",
        "messages": [
            {
                "role": "assistant",
                "content": "Let's talk about design. What are you building?",
            }
        ],
    },
    {
        "id": 3,
        "name": "Deployment Tips",
        "messages": [
            {
                "role": "assistant",
                "content": "Deploying your app is the final step. I can give you some tips.",
            }
        ],
    },
]


class ChatState(rx.State):
    conversations: list[Conversation] = initial_conversations
    active_conversation_id: int = 1
    current_message: str = ""
    is_processing: bool = False
    sidebar_open: bool = True

    @rx.var
    def active_conversation(self) -> Conversation | None:
        for conv in self.conversations:
            if conv["id"] == self.active_conversation_id:
                return conv
        return None

    @rx.var
    def messages(self) -> list[Message]:
        active_conv = self.active_conversation
        return active_conv["messages"] if active_conv else []

    @rx.event
    def set_active_conversation(self, conv_id: int):
        self.active_conversation_id = conv_id
        if self.sidebar_open:
            self.sidebar_open = False

    @rx.event
    def set_current_message(self, value: str):
        self.current_message = value

    @rx.event(background=True)
    async def send_message(self):
        async with self:
            if not self.current_message.strip() or self.is_processing:
                return
            self.is_processing = True
            for conv in self.conversations:
                if conv["id"] == self.active_conversation_id:
                    conv["messages"].append(
                        {"role": "user", "content": self.current_message}
                    )
                    break
            self.current_message = ""
            yield
        await asyncio.sleep(1)
        async with self:
            for conv in self.conversations:
                if conv["id"] == self.active_conversation_id:
                    conv["messages"].append({"role": "assistant", "content": ""})
                    break
            yield
        await asyncio.sleep(0.5)
        response_text = """This is a **simulated** response from the `assistant`.

Reflex makes building UIs like this a breeze!

Here is a list of things you can ask me:
- How to use `rx.cond`
- What are computed vars?
- Show me an example of a `for` loop."""
        for i in range(len(response_text) + 1):
            async with self:
                for conv in self.conversations:
                    if conv["id"] == self.active_conversation_id:
                        conv["messages"][-1]["content"] = response_text[:i]
                        break
            await asyncio.sleep(0.02)
        async with self:
            self.is_processing = False

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open
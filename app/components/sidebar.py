import reflex as rx
from app.states.chat_state import ChatState
from app.states.auth_state import AuthState


def conversation_item(conv: dict) -> rx.Component:
    return rx.el.div(
        rx.el.a(
            rx.icon("message-circle", class_name="h-4 w-4 shrink-0 text-gray-500"),
            rx.el.span(conv["name"], class_name="truncate"),
            on_click=lambda: ChatState.set_active_conversation(conv["id"]),
            class_name=rx.cond(
                ChatState.active_conversation_id == conv["id"],
                "flex items-center gap-3 rounded-lg bg-blue-100 px-3 py-2 text-blue-600 font-semibold transition-all hover:text-blue-700",
                "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:bg-gray-100 hover:text-gray-900",
            ),
        ),
        class_name="w-full",
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "bot-message-square", class_name="h-8 w-8 text-blue-600"
                        ),
                        rx.el.h1(
                            "Reflex Chat", class_name="text-xl font-bold text-gray-800"
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5"),
                        on_click=ChatState.toggle_sidebar,
                        class_name="p-2 md:hidden",
                    ),
                    class_name="flex h-16 items-center justify-between border-b px-4 lg:h-[60px] lg:px-6",
                )
            ),
            rx.el.div(
                rx.el.nav(
                    rx.foreach(ChatState.conversations, conversation_item),
                    class_name="flex flex-col gap-1 p-2",
                ),
                class_name="flex-1 overflow-auto py-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.button(
                            rx.icon("log-out", class_name="mr-2 h-4 w-4"),
                            "Logout",
                            on_click=AuthState.logout,
                            class_name="w-full flex items-center justify-center bg-gray-200 text-gray-600 text-sm font-medium py-2 px-3 rounded-lg hover:bg-gray-300 transition-colors",
                        ),
                        class_name="p-4",
                    )
                ),
                class_name="mt-auto border-t",
            ),
            class_name="flex h-full max-h-screen flex-col",
        ),
        class_name=rx.cond(
            ChatState.sidebar_open,
            "h-full w-full md:w-64 lg:w-72 bg-gray-50 border-r transition-transform transform translate-x-0",
            "h-full w-full md:w-64 lg:w-72 bg-gray-50 border-r transition-transform transform -translate-x-full md:translate-x-0",
        ),
    )
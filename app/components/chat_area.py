import reflex as rx
from app.states.chat_state import ChatState, Message


def message_bubble(message: Message) -> rx.Component:
    is_user = message["role"] == "user"
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=rx.cond(
                        is_user,
                        f"https://api.dicebear.com/9.x/initials/svg?seed=User",
                        f"https://api.dicebear.com/9.x/bottts-neutral/svg?seed=Reflex",
                    ),
                    class_name="h-8 w-8 rounded-full",
                ),
                rx.el.div(
                    rx.markdown(
                        message["content"],
                        class_name="prose prose-sm max-w-full break-words",
                        background="transparent",
                        component_map={
                            "a": lambda text, **props: rx.el.a(
                                text,
                                **props,
                                class_name="text-current font-bold underline",
                            ),
                            "p": lambda text: rx.el.p(text, class_name="text-current"),
                            "ul": lambda text: rx.el.ul(
                                text, class_name="list-disc pl-5 text-current"
                            ),
                            "ol": lambda text: rx.el.ol(
                                text, class_name="list-decimal pl-5 text-current"
                            ),
                            "code": lambda text: rx.el.code(
                                text,
                                class_name="bg-gray-300 text-gray-800 rounded px-1 py-0.5 font-mono text-xs",
                            ),
                        },
                    ),
                    class_name=rx.cond(
                        is_user,
                        "p-3 rounded-lg rounded-bl-none bg-blue-600 text-white",
                        "p-3 rounded-lg rounded-br-none bg-gray-200 text-gray-800",
                    ),
                ),
                rx.cond(
                    ~is_user,
                    rx.el.button(
                        rx.icon("copy", class_name="h-4 w-4 text-gray-500"),
                        on_click=[
                            rx.set_clipboard(message["content"]),
                            rx.toast("Copied to clipboard", duration=3000),
                        ],
                        class_name="p-1 rounded-md hover:bg-gray-300 transition-colors",
                    ),
                    None,
                ),
                class_name=rx.cond(
                    is_user,
                    "flex items-start gap-3 justify-end",
                    "flex items-start gap-3",
                ),
            ),
            class_name="max-w-4xl w-full mx-auto",
        ),
        class_name=rx.cond(
            is_user, "flex justify-end w-full", "flex justify-start w-full"
        ),
    )


def chat_header() -> rx.Component:
    return rx.el.header(
        rx.el.button(
            rx.icon("panel-left", class_name="h-5 w-5"),
            on_click=ChatState.toggle_sidebar,
            class_name="p-2 md:hidden",
        ),
        rx.el.div(
            rx.el.h2(
                ChatState.active_conversation.name,
                class_name="text-lg font-semibold text-gray-800",
            ),
            class_name="flex-1 text-center",
        ),
        rx.el.div(class_name="w-8"),
        class_name="flex h-16 items-center justify-between border-b bg-gray-50 px-4",
    )


def message_input() -> rx.Component:
    return rx.el.div(
        rx.el.form(
            rx.el.div(
                rx.el.textarea(
                    placeholder="Type your message...",
                    on_change=ChatState.set_current_message,
                    rows=1,
                    class_name="w-full resize-none border-0 bg-transparent p-3 pr-10 text-sm placeholder-gray-400 focus:ring-0",
                    default_value=ChatState.current_message,
                ),
                rx.el.button(
                    rx.icon("send", class_name="h-5 w-5"),
                    type="submit",
                    disabled=ChatState.is_processing
                    | (ChatState.current_message.strip() == ""),
                    class_name="absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-full text-blue-600 disabled:text-gray-400 disabled:cursor-not-allowed hover:bg-blue-100 transition-colors",
                ),
                class_name="relative flex-1",
            ),
            on_submit=ChatState.send_message,
            reset_on_submit=True,
            class_name="w-full",
        ),
        class_name="mx-auto w-full max-w-4xl rounded-lg border bg-white shadow-sm",
    )


def chat_area() -> rx.Component:
    return rx.el.div(
        chat_header(),
        rx.el.main(
            rx.el.div(
                rx.foreach(ChatState.messages, message_bubble),
                rx.cond(
                    ChatState.is_processing,
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=f"https://api.dicebear.com/9.x/bottts-neutral/svg?seed=Reflex",
                                class_name="h-8 w-8 rounded-full",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    class_name="h-2 w-2 rounded-full bg-gray-400 animate-pulse"
                                ),
                                rx.el.div(
                                    class_name="h-2 w-2 rounded-full bg-gray-400 animate-pulse",
                                    style={"animation_delay": "0.2s"},
                                ),
                                rx.el.div(
                                    class_name="h-2 w-2 rounded-full bg-gray-400 animate-pulse",
                                    style={"animation_delay": "0.4s"},
                                ),
                                class_name="flex gap-1 items-center p-3",
                            ),
                            class_name="flex items-start gap-3",
                        ),
                        class_name="max-w-4xl w-full mx-auto flex justify-start",
                    ),
                    None,
                ),
                id="chat-messages",
                class_name="space-y-6 p-4 md:p-6",
            ),
            class_name="flex-1 overflow-auto",
        ),
        rx.el.footer(message_input(), class_name="border-t bg-gray-50 p-4"),
        class_name="flex h-screen flex-col",
    )
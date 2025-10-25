import reflex as rx
from app.components.sidebar import sidebar
from app.components.chat_area import chat_area
from app.states.auth_state import AuthState


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            sidebar(),
            class_name="fixed inset-y-0 left-0 z-20 h-full md:static md:z-auto",
        ),
        rx.el.div(chat_area(), class_name="flex-1 md:ml-64 lg:ml-72"),
        class_name="flex min-h-screen w-full bg-white font-['Open_Sans']",
    )


def login() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("bot-message-square", class_name="h-8 w-8 text-blue-600"),
                rx.el.h2("Welcome Back", class_name="text-2xl font-bold text-gray-800"),
                class_name="flex flex-col items-center gap-4",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Email", class_name="text-sm font-medium text-gray-600"
                    ),
                    rx.el.input(
                        placeholder="user@example.com",
                        name="email",
                        type="email",
                        class_name="mt-1 w-full rounded-lg border border-gray-300 p-2 text-sm focus:border-blue-500 focus:ring-blue-500",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password", class_name="text-sm font-medium text-gray-600"
                    ),
                    rx.el.div(
                        rx.el.input(
                            placeholder="password",
                            name="password",
                            type=rx.cond(AuthState.show_password, "text", "password"),
                            class_name="mt-1 w-full rounded-lg border border-gray-300 p-2 text-sm focus:border-blue-500 focus:ring-blue-500",
                        ),
                        rx.el.button(
                            rx.icon(
                                rx.cond(AuthState.show_password, "eye-off", "eye"),
                                class_name="h-4 w-4",
                            ),
                            on_click=AuthState.toggle_show_password,
                            type="button",
                            class_name="absolute inset-y-0 right-0 flex items-center px-3 text-gray-500 hover:text-gray-700",
                        ),
                        class_name="relative",
                    ),
                    class_name="w-full",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        rx.icon("flag_triangle_right", class_name="h-4 w-4 mr-2"),
                        rx.el.p(AuthState.error_message, class_name="text-sm"),
                        class_name="flex items-center p-2 bg-red-100 text-red-700 rounded-lg w-full",
                    ),
                    None,
                ),
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="checkbox", name="remember_me", class_name="mr-2"
                        ),
                        "Remember me",
                        class_name="flex items-center text-sm text-gray-600",
                    ),
                    rx.el.a(
                        "Forgot password?",
                        href="#",
                        class_name="text-sm text-blue-600 hover:underline",
                    ),
                    class_name="flex items-center justify-between w-full",
                ),
                rx.el.button(
                    "Login",
                    type="submit",
                    class_name="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-300 disabled:cursor-not-allowed",
                ),
                on_submit=AuthState.login,
                reset_on_submit=True,
                class_name="flex flex-col items-center gap-4 w-full",
            ),
            class_name="flex flex-col items-center gap-6 w-full max-w-sm p-8 bg-white rounded-2xl shadow-sm border",
        ),
        class_name="flex min-h-screen w-full items-center justify-center bg-gray-50 font-['Open_Sans']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=AuthState.check_login)
app.add_page(login, route="/login")
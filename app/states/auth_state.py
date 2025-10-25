import reflex as rx
import asyncio


class AuthState(rx.State):
    email: str = ""
    password: str = ""
    remember_me: bool = False
    is_logged_in: bool = False
    error_message: str = ""
    show_password: bool = False

    @rx.event
    async def login(self, form_data: dict):
        """Login the user."""
        self.email = form_data.get("email", "").strip()
        self.password = form_data.get("password", "").strip()
        self.remember_me = bool(form_data.get("remember_me", False))
        self.error_message = ""
        if not self.email or not self.password:
            self.error_message = "Email and password are required."
            return
        await asyncio.sleep(1)
        if self.email == "user@example.com" and self.password == "password":
            self.is_logged_in = True
            return rx.redirect("/")
        else:
            self.error_message = "Invalid email or password."

    @rx.event
    def logout(self):
        """Logout the user."""
        self.is_logged_in = False
        self.email = ""
        self.password = ""
        self.remember_me = False
        return rx.redirect("/login")

    @rx.event
    def toggle_show_password(self):
        self.show_password = not self.show_password

    @rx.var
    def is_form_valid(self) -> bool:
        return self.email != "" and self.password != ""

    @rx.event
    def check_login(self):
        if not self.is_logged_in:
            return rx.redirect("/login")
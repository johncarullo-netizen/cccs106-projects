# main.py
import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact, toggle_theme

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    
    db_conn = init_db()
    
    # Input fields
    name_input = ft.TextField(label="Name", width=350)
    phone_input = ft.TextField(label="Phone", width=350)
    email_input = ft.TextField(label="Email", width=350)
    inputs = (name_input, phone_input, email_input)
    
    # Search field
    search_input = ft.TextField(
        label="Search contacts by name",
        width=350,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: display_contacts(page, contacts_list_view, db_conn, e.control.value)
    )
    
    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)
    
    # Add contact button
    add_button = ft.ElevatedButton(
        text="Add Contact",
        icon=ft.Icons.ADD,
        on_click=lambda e: add_contact(page, inputs, contacts_list_view, db_conn, search_input)
    )
    
    # Theme toggle switch
    theme_switch = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="Toggle Dark/Light Mode",
        on_click=lambda e: toggle_theme(page)
    )
    
    # Header with theme toggle
    header = ft.Row(
        [
            ft.Text("Contact Book", size=24, weight=ft.FontWeight.BOLD),
            theme_switch,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    page.add(
        ft.Column(
            [
                header,
                ft.Divider(),
                ft.Text("Enter Contact Details:", size=18, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                ft.Divider(height=20),
                ft.Text("Contacts:", size=18, weight=ft.FontWeight.BOLD),
                search_input,
                contacts_list_view,
            ]
        )
    )
    
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)
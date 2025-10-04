# app_logic.py
import flet as ft
from database import update_contact_db, delete_contact_db, add_contact_db, get_all_contacts_db

def display_contacts(page, contacts_list_view, db_conn, search_term=""):
    """Fetches and displays all contacts in the ListView with optional search filter."""
    contacts_list_view.controls.clear()
    contacts = get_all_contacts_db(db_conn, search_term)
    
    for contact in contacts:
        contact_id, name, phone, email = contact
        
        # Create a modern card design with icons
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE),
                            title=ft.Text(name, weight=ft.FontWeight.BOLD, size=16),
                            trailing=ft.PopupMenuButton(
                                icon=ft.Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(
                                        text="Edit",
                                        icon=ft.Icons.EDIT,
                                        on_click=lambda _, c=contact: open_edit_dialog(page, c, db_conn, contacts_list_view, search_term)
                                    ),
                                    ft.PopupMenuItem(),
                                    ft.PopupMenuItem(
                                        text="Delete",
                                        icon=ft.Icons.DELETE,
                                        on_click=lambda _, cid=contact_id: open_delete_confirmation(page, cid, db_conn, contacts_list_view, search_term)
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.PHONE, size=16, color=ft.Colors.GREEN),
                                            ft.Text(phone if phone else "No phone", size=14),
                                        ],
                                        spacing=5,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.EMAIL, size=16, color=ft.Colors.ORANGE),
                                            ft.Text(email if email else "No email", size=14),
                                        ],
                                        spacing=5,
                                    ),
                                ],
                                spacing=5,
                            ),
                            padding=ft.padding.only(left=15, right=15, bottom=10),
                        ),
                    ],
                    spacing=0,
                ),
                padding=5,
            ),
        )
        
        contacts_list_view.controls.append(card)
    
    page.update()

def add_contact(page, inputs, contacts_list_view, db_conn, search_input=None):
    """Adds a new contact with input validation and refreshes the list."""
    name_input, phone_input, email_input = inputs
    
    # Input validation: Check if name is empty
    if not name_input.value or name_input.value.strip() == "":
        name_input.error_text = "Name cannot be empty"
        page.update()
        return
    
    # Clear any previous error
    name_input.error_text = None
    
    add_contact_db(db_conn, name_input.value.strip(), phone_input.value, email_input.value)
    
    for field in inputs:
        field.value = ""
    
    search_term = search_input.value if search_input else ""
    display_contacts(page, contacts_list_view, db_conn, search_term)
    page.update()

def open_delete_confirmation(page, contact_id, db_conn, contacts_list_view, search_term=""):
    """Opens a confirmation dialog before deleting a contact."""
    
    def confirm_delete(e):
        delete_contact_db(db_conn, contact_id)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn, search_term)
    
    def cancel_delete(e):
        dialog.open = False
        page.update()
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirm Delete"),
        content=ft.Text("Are you sure you want to delete this contact?"),
        actions=[
            ft.TextButton("No", on_click=cancel_delete),
            ft.TextButton("Yes", on_click=confirm_delete),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.open(dialog)

def delete_contact(page, contact_id, db_conn, contacts_list_view, search_term=""):
    """Deletes a contact and refreshes the list."""
    delete_contact_db(db_conn, contact_id)
    display_contacts(page, contacts_list_view, db_conn, search_term)

def open_edit_dialog(page, contact, db_conn, contacts_list_view, search_term=""):
    """Opens a dialog to edit a contact's details."""
    contact_id, name, phone, email = contact
    
    edit_name = ft.TextField(label="Name", value=name)
    edit_phone = ft.TextField(label="Phone", value=phone)
    edit_email = ft.TextField(label="Email", value=email)
    
    def save_and_close(e):
        # Validate name before saving
        if not edit_name.value or edit_name.value.strip() == "":
            edit_name.error_text = "Name cannot be empty"
            page.update()
            return
        
        update_contact_db(db_conn, contact_id, edit_name.value.strip(), edit_phone.value, edit_email.value)
        dialog.open = False
        page.update()
        display_contacts(page, contacts_list_view, db_conn, search_term)
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Contact"),
        content=ft.Column([edit_name, edit_phone, edit_email], tight=True),
        actions=[
            ft.TextButton("Cancel", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
            ft.TextButton("Save", on_click=save_and_close),
        ],
    )
    
    page.open(dialog)

def toggle_theme(page):
    """Toggles between light and dark mode."""
    if page.theme_mode == ft.ThemeMode.LIGHT:
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    page.update()
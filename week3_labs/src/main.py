# main.py
# CCCS 106 - Week 3 Lab Exercise
# User Login Application with MySQL Database

import flet as ft
import mysql.connector
from db_connection import connect_db

def main(page: ft.Page):
    # Page configuration
    page.window.center()
    page.window.frameless = True
    page.title = "User Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 350
    page.window.width = 400
    page.bgcolor = "#FFD54F"  # Yellow background matching the image
    
    # UI Controls
    # Login Title
    login_title = ft.Text(
        "User Login",
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.BLACK87
    )
    
    # Username Input Field
    username_field = ft.TextField(
        label="User name",
        hint_text="Enter your user name",
        helper_text="This is your unique identifier",
        width=300,
        autofocus=True,
        disabled=False,
        prefix_icon=ft.Icons.PERSON,
        bgcolor="#4FC3F7",  # Light blue matching the image
        color=ft.Colors.BLACK,
        border_color="#4FC3F7",
        focused_border_color="#29B6F6",
        label_style=ft.TextStyle(color="#1976D2"),
        helper_style=ft.TextStyle(color=ft.Colors.BLACK54)
    )
    
    # Password Input Field
    password_field = ft.TextField(
        label="Password",
        hint_text="Enter your password",
        helper_text="This is your secret key",
        width=300,
        disabled=False,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK,
        bgcolor="#4FC3F7",  # Light blue matching the image
        color=ft.Colors.BLACK,
        border_color="#4FC3F7",
        focused_border_color="#29B6F6",
        label_style=ft.TextStyle(color="#1976D2"),
        helper_style=ft.TextStyle(color=ft.Colors.BLACK54)
    )
    
    # Login Logic
    async def login_click(e):
        # Define Dialogs for Feedback
        success_dialog = ft.AlertDialog(
            title=ft.Text("Login Successful"),
            content=ft.Text(
                f"Welcome, {username_field.value}!",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(success_dialog))
            ],
            icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=40)
        )
        
        failure_dialog = ft.AlertDialog(
            title=ft.Text("Login Failed"),
            content=ft.Text(
                "Invalid username or password",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(failure_dialog))
            ],
            icon=ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=40)
        )
        
        invalid_input_dialog = ft.AlertDialog(
            title=ft.Text("Input Error"),
            content=ft.Text(
                "Please enter username and password",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(invalid_input_dialog))
            ],
            icon=ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE, size=40)
        )
        
        database_error_dialog = ft.AlertDialog(
            title=ft.Text("Database Error"),
            content=ft.Text(
                "An error occurred while connecting to the database",
                text_align=ft.TextAlign.CENTER
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(database_error_dialog))
            ]
        )
        
        # Helper function to close dialogs
        def close_dialog(dialog):
            dialog.open = False
            page.update()
        
        # Validation and Database Logic
        # Check if username or password are empty
        if not username_field.value or not password_field.value:
            page.overlay.append(invalid_input_dialog)
            invalid_input_dialog.open = True
            page.update()
            return
        
        # Database authentication
        try:
            # Establish database connection
            connection = connect_db()
            cursor = connection.cursor()
            
            # Execute parameterized SQL query (prevents SQL injection)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username_field.value, password_field.value))
            
            # Fetch the result
            result = cursor.fetchone()
            
            # Close the database connection
            cursor.close()
            connection.close()
            
            # Check if user was found
            if result:
                page.overlay.append(success_dialog)
                success_dialog.open = True
            else:
                page.overlay.append(failure_dialog)
                failure_dialog.open = True
            
            page.update()
            
        except mysql.connector.Error as err:
            page.overlay.append(database_error_dialog)
            database_error_dialog.open = True
            page.update()
    
    # Login Button
    login_button = ft.ElevatedButton(
        text="Login",
        on_click=login_click,
        width=100,
        icon=ft.Icons.LOGIN,
        bgcolor=ft.Colors.WHITE,
        color=ft.Colors.BLUE_700
    )
    
    # Add all controls to the page
    page.add(
        login_title,
        ft.Container(
            content=ft.Column(
                [
                    username_field,
                    password_field
                ],
                spacing=20
            )
        ),
        ft.Container(
            content=login_button,
            alignment=ft.alignment.top_right,
            margin=ft.margin.only(top=0, right=20, bottom=40, left=0)
        )
    )

# Start the Flet app
if __name__ == "__main__":
    ft.app(target=main)
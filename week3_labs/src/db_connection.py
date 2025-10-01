
# db_connection.py
# CCCS 106 - Week 3 Lab Exercise
# Database Connection Module

import mysql.connector

def connect_db():
    """Establishes connection to MySQL database"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="newpassword",  # IMPORTANT: Replace with your MySQL password
        database="fletapp"
    )
    return connection
import streamlit as st
import mysql.connector
from cryptography.fernet import Fernet
import pandas as pd
# Encryption key
key = b'xxTTd0bS9SR76fltNELEV5pJbRhKLfK0xEtSiBv0EgA='

# Encrypt data using the key
def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    try:
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        return decrypted_data.decode()
    except Exception as e:
        print("Error during decryption:", e)
        return None

# Function to connect to MySQL database
def connect_to_database(host, username, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None, None
# Function to decrypt all data from the database
# def decrypt_all_data(cursor):
#     cursor.execute("SELECT * FROM students")
#     records = cursor.fetchall()
#     decrypted_records = []
#     for record in records:
#         decrypted_record = []
#         for field in record:
#             if isinstance(field, bytes):
#                 decrypted_field = decrypt_data(field, key)
#                 decrypted_record.append(decrypted_field)
#             else:
#                 decrypted_record.append(field)
#         decrypted_records.append(decrypted_record)
#     return decrypted_records

# def decrypt_all_data(cursor, key):
#     try:
#         cursor.execute("SELECT * FROM students")
#         records = cursor.fetchall()
#         decrypted_records = []
#         for record in records:
#             decrypted_record = []
#             for field in record:
#                 if isinstance(field, bytes):
#                     decrypted_field = decrypt_data(field, key)
#                     decrypted_record.append(decrypted_field)
#                 else:
#                     decrypted_record.append(field)
#             decrypted_records.append(decrypted_record)
#         return decrypted_records
#     except mysql.connector.Error as e:
#         print(f"Error fetching and decrypting data: {e}")
#         return []
def fetch_encrypted_data(cursor):
    try:
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        st.error(f"Error fetching data from database: {e}")
        return []

def decrypt_all_data(cursor, key):
    records = fetch_encrypted_data(cursor)
    decrypted_records = []
    for record in records:
        decrypted_record = []
        for field in record:
            if isinstance(field, bytes):
                decrypted_field = decrypt_data(field, key)
                decrypted_record.append(decrypted_field)
            else:
                decrypted_record.append(field)
        decrypted_records.append(decrypted_record)
    return decrypted_records

st.title("Encrypted Database Management System")

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Connect to Database", "Search", "CRUD"])

# Page: Connect to Database
if page == "Connect to Database":
    st.header("Connect to Database")
    host = st.text_input("MySQL Host", "localhost")
    username = st.text_input("MySQL Username", "")
    password = st.text_input("MySQL Password", "", type="password")
    database = st.text_input("MySQL Database", "")
    if st.button("Connect"):
        conn, cursor = connect_to_database(host, username, password, database)
        if conn:
            st.success("Connected to MySQL database successfully!")
            st.session_state.cursor = cursor
            st.session_state.conn = conn
        else:
            st.error("Failed to connect to MySQL database.")

# Page: CRUD
elif page == "CRUD":
    st.header("CRUD Operations")
    if "cursor" in st.session_state:
        action = st.selectbox("Select Action", ["Create", "Read", "Update", "Delete"])
        
        if action == "Create":
            st.subheader("Create Record")
            roll_no = st.text_input("Roll No")
            name = st.text_input("Name")
            department = st.text_input("Department")
            section = st.text_input("Section")
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            address = st.text_input("Address")
            cgpa = st.number_input("CGPA", min_value=0.0)
            blood_group = st.text_input("Blood Group")
            father_name = st.text_input("Father's Name")
            if st.button("Create Record"):
                try:
                    # Encrypt sensitive data
                    encrypted_roll_no = encrypt_data(roll_no, key)
                    encrypted_name = encrypt_data(name, key)
                    encrypted_department = encrypt_data(department, key)
                    encrypted_section = encrypt_data(section, key)
                    encrypted_email = encrypt_data(email, key)
                    encrypted_phone_number = encrypt_data(phone_number, key)
                    encrypted_address = encrypt_data(address, key)
                    encrypted_blood_group = encrypt_data(blood_group, key)
                    encrypted_father_name = encrypt_data(father_name, key)
                    query = "INSERT INTO students (roll_no, name, department, section, email, phone_number, address, cgpa, blood_group, father_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    st.session_state.cursor.execute(query, (encrypted_roll_no, encrypted_name, encrypted_department, encrypted_section, encrypted_email, encrypted_phone_number, encrypted_address, cgpa, encrypted_blood_group, encrypted_father_name))
                    st.session_state.conn.commit()
                    st.success("Record created successfully!")
                except mysql.connector.Error as e:
                    st.error(f"Error creating record: {e}")
        
        elif action == "Read":
            st.subheader("Read Records")
            st.write("Displaying all records from the 'students' table:")
            st.session_state.cursor.execute("SELECT * FROM students")
            records = st.session_state.cursor.fetchall()
            for record in records:
                # Decrypt sensitive data
                decrypted_record = [decrypt_data(field, key) if isinstance(field, bytes) else field for field in record]
                st.write(decrypted_record)
        
        elif action == "Update":
            st.subheader("Update Record")
            record_id = st.text_input("Enter Record ID to Update")
            roll_no = st.text_input("Roll No")
            name = st.text_input("Name")
            department = st.text_input("Department")
            section = st.text_input("Section")
            email = st.text_input("Email")
            phone_number = st.text_input("Phone Number")
            address = st.text_input("Address")
            cgpa = st.number_input("CGPA", min_value=0.0)
            blood_group = st.text_input("Blood Group")
            father_name = st.text_input("Father's Name")
            if st.button("Update Record"):
                try:
                    # Encrypt sensitive data
                    encrypted_roll_no = encrypt_data(roll_no, key)
                    encrypted_name = encrypt_data(name, key)
                    encrypted_department = encrypt_data(department, key)
                    encrypted_section = encrypt_data(section, key)
                    encrypted_email = encrypt_data(email, key)
                    encrypted_phone_number = encrypt_data(phone_number, key)
                    encrypted_address = encrypt_data(address, key)
                    encrypted_blood_group = encrypt_data(blood_group, key)
                    encrypted_father_name = encrypt_data(father_name, key)
                    query = "UPDATE students SET roll_no=%s, name=%s, department=%s, section=%s, email=%s, phone_number=%s, address=%s, cgpa=%s, blood_group=%s, father_name=%s WHERE id=%s"
                    st.session_state.cursor.execute(query, (encrypted_roll_no, encrypted_name, encrypted_department, encrypted_section, encrypted_email, encrypted_phone_number, encrypted_address, cgpa, encrypted_blood_group, encrypted_father_name, record_id))
                    st.session_state.conn.commit()
                    if st.session_state.cursor.rowcount > 0:
                        st.success("Record updated successfully!")
                    else:
                        st.warning("No records updated.")
                except mysql.connector.Error as e:
                    st.error(f"Error updating record: {e}")
        
        elif action == "Delete":
            st.subheader("Delete Record")
            record_id = st.text_input("Enter Record ID to Delete")
            if st.button("Delete Record"):
                try:
                    query = "DELETE FROM students WHERE id=%s"
                    st.session_state.cursor.execute(query, (record_id,))
                    st.session_state.conn.commit()
                    if st.session_state.cursor.rowcount > 0:
                        st.success("Record deleted successfully!")
                    else:
                        st.warning("No records deleted.")
                except mysql.connector.Error as e:
                    st.error(f"Error deleting record: {e}")
    else:
        st.warning("Please connect to the database first.")
# Page: Search
elif page == "Search":
    st.header("Search Records")
    if "cursor" in st.session_state:
        try:
            # Fetch and decrypt all data from the database
            decrypted_records = decrypt_all_data(st.session_state.cursor, key)

            
            # Start search
            search_pattern = st.text_input("Enter search pattern:", "")
            if st.button("Search"):
                if search_pattern:
                    matching_records = []
                    # Perform substring matching on all fields after decryption
                    for record in decrypted_records:
                        for field in record:
                            if isinstance(field, str) and search_pattern.lower() in field.lower():
                                matching_records.append(record)
                                break
                    if matching_records:
                        st.write("Search Results:")
                        # Display matching records in a table
                        df = pd.DataFrame(matching_records)
                        st.dataframe(df)
                    else:
                        st.write("No results found.")
                else:
                    st.write("Please enter a search pattern.")
        except mysql.connector.Error as e:
            st.error(f"Error fetching and decrypting records: {e}")
    else:
        st.warning("Please connect to the database first.")

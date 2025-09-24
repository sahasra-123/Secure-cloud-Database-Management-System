import mysql.connector
import pandas as pd
from cryptography.fernet import Fernet
import streamlit as st
from wordcloud import WordCloud

# -----------------------------
# CONFIG
# -----------------------------
# !!! Put your real MySQL root password here !!!
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"      # <- <-- FILL THIS IN
DB_NAME = "student_database"

# One stable Fernet key. Use the same key for encrypt/decrypt of existing rows.
# If you change this, old rows won't decrypt.
key = b'xxTTd0bS9SR76fltNELEV5pJbRhKLfK0xEtSiBv0EgA='

# -----------------------------
# ENCRYPT / DECRYPT HELPERS
# -----------------------------
def encrypt_data(data: str, key: bytes) -> str:
    """Encrypts a string and returns a UTF-8 string token (safe to store in TEXT)."""
    if data is None:
        data = ""
    cipher = Fernet(key)
    token_bytes = cipher.encrypt(data.encode("utf-8"))
    return token_bytes.decode("utf-8")  # store as TEXT

def _to_bytes_for_decrypt(value):
    """Accept str/bytes/bytearray from DB and return bytes token for Fernet."""
    if value is None:
        return None
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    # Fallback: convert to string
    return str(value).encode("utf-8")

def decrypt_data(encrypted_value, key: bytes):
    """Decrypts a value that may be str/bytes/bytearray. Returns str or None on failure."""
    try:
        token = _to_bytes_for_decrypt(encrypted_value)
        if token is None:
            return None
        cipher = Fernet(key)
        return cipher.decrypt(token).decode("utf-8")
    except Exception:
        return None

def decrypt_record(row):
    """Decrypts each field in a DB row; leaves numbers alone."""
    out = []
    for field in row:
        if isinstance(field, (str, bytes, bytearray)):
            out.append(decrypt_data(field, key))
        else:
            out.append(field)
    return out

# -----------------------------
# DB
# -----------------------------
def connect_to_database(host, username, password, database):
    try:
        conn = mysql.connector.connect(
            host=host, user=username, password=password, database=database
        )
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None, None

def fetch_encrypted_data(cursor):
    try:
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()
    except mysql.connector.Error as e:
        st.error(f"Error fetching data from database: {e}")
        return []

def insert_data(cursor, data_tuple):
    try:
        cursor.execute(
            """
            INSERT INTO students
            (id, roll_no, name, department, section, email, phone_number, address, cgpa, blood_group, father_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            data_tuple,
        )
        # IMPORTANT: commit from the cursor's connection
        cursor.connection.commit()
    except mysql.connector.Error as e:
        st.error(f"Error inserting data into database: {e}")

# -----------------------------
# UI PAGES
# -----------------------------
def home():
    st.title("Accelerated Searchable Encrypted Database Management Systems for Cloud Services")
    st.header("Welcome to the AESDBMS Cloud Platform")
    st.markdown(
        """
        :cloud: **AESDBMS Cloud Platform**: Experience the power of secure and efficient database management in the cloud.

        **Features**
        - :closed_lock_with_key: **Encryption**
        - :mag_right: **Accelerated Search**
        - :chart_with_upwards_trend: **Scalability**
        - :cloud: **Cloud Integration**
        - :floppy_disk: **Data Management**
        """
    )

def insert_form(cursor):
    st.title("Insert Data into Database")
    st.write("Fill in the following fields to insert a new student record into the database.")

    id = st.number_input("ID", min_value=1, step=1)
    roll_no = st.number_input("Roll No", min_value=1, step=1)
    name = st.text_input("Name")
    department = st.text_input("Department")
    section = st.text_input("Section")
    email = st.text_input("Email")
    phone_number = st.text_input("Phone Number")
    address = st.text_input("Address")
    cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, step=0.01)
    blood_group = st.text_input("Blood Group")
    father_name = st.text_input("Father's Name")

    st.caption("The entered data will be encrypted before being stored.")

    if st.button("Insert Data"):
        encrypted_row = (
            id,
            roll_no,
            encrypt_data(name, key),
            encrypt_data(department, key),
            encrypt_data(section, key),
            encrypt_data(email, key),
            encrypt_data(phone_number, key),
            encrypt_data(address, key),
            cgpa,
            encrypt_data(blood_group, key),
            encrypt_data(father_name, key),
        )
        insert_data(cursor, encrypted_row)
        st.success("Data inserted successfully!")

def search(cursor):
    st.title("Search Data")
    term = st.text_input("Search (substring)", placeholder="Enter search term...").strip()

    if st.button("Search"):
        encrypted_rows = fetch_encrypted_data(cursor)
        if not encrypted_rows:
            st.warning("No encrypted data found in the database.")
            return

        results = []
        for row in encrypted_rows:
            dec = decrypt_record(row)
            if any(term.lower() in str(v).lower() for v in dec if v is not None):
                results.append(dec)

        if results:
            headers = [col[0] for col in cursor.description]
            st.subheader("Search Results")
            st.table(pd.DataFrame(results, columns=headers))
        else:
            st.info("No matching records found.")

def display_encrypted_database(cursor):
    st.title("Encrypted Database")
    encrypted_rows = fetch_encrypted_data(cursor)
    if encrypted_rows:
        headers = [col[0] for col in cursor.description]
        st.table(pd.DataFrame(encrypted_rows, columns=headers))
    else:
        st.warning("No encrypted data found in the database.")

def execute_query(cursor, query):
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            headers = [c[0] for c in cursor.description]
            dec_rows = [decrypt_record(r) for r in rows]
            st.subheader("Query Results")
            st.table(pd.DataFrame(dec_rows, columns=headers))
        else:
            st.info("No records found for the given query.")
    except mysql.connector.Error as e:
        st.error(f"Error executing query: {e}")

def execute_query_page(cursor):
    st.title("Execute Searchable Queries")
    q = st.text_area("Query")
    if st.button("Execute"):
        if q.strip():
            execute_query(cursor, q)
        else:
            st.warning("Please enter a valid SQL query.")

def full_data(cursor):
    st.title("Full Data")
    rows = fetch_encrypted_data(cursor)
    if not rows:
        st.warning("No encrypted data found in the database.")
        return None
    headers = [c[0] for c in cursor.description]
    dec = [decrypt_record(r) for r in rows]
    df = pd.DataFrame(dec, columns=headers)
    st.table(df)
    return df

def display_visualizations(decrypted_df):
    # Department distribution
    st.subheader('Distribution of Students Across Departments')
    dept_counts = decrypted_df['department'].value_counts()
    st.bar_chart(dept_counts)

    # Average CGPA per department
    st.subheader('CGPA in Department')
    cgpa_department = decrypted_df.groupby('department')['cgpa'].mean().reset_index()
    st.bar_chart(cgpa_department.set_index('department'))

    # Word cloud for father's names
    st.subheader("Word Cloud of Father's Names")
    names = decrypted_df['father_name'].dropna().tolist()
    wc = WordCloud(width=800, height=400, background_color='white').generate(' '.join(names))
    st.image(wc.to_array())

def visualizations_page(cursor):
    df = full_data(cursor)
    if df is not None and not df.empty:
        display_visualizations(df)
    else:
        st.warning("No data to visualize.")

# -----------------------------
# MAIN
# -----------------------------
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Insert Data", "Search", "Full Data",
                                      "Encrypted Database", "Visualizations", "Execute Query"])

    conn, cursor = connect_to_database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

    if not conn:
        st.error("Failed to connect to MySQL database. Check your credentials/server.")
        return

    try:
        if page == "Home":
            home()
        elif page == "Insert Data":
            insert_form(cursor)
        elif page == "Search":
            search(cursor)
        elif page == "Full Data":
            full_data(cursor)
        elif page == "Encrypted Database":
            display_encrypted_database(cursor)
        elif page == "Visualizations":
            visualizations_page(cursor)
        elif page == "Execute Query":
            execute_query_page(cursor)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

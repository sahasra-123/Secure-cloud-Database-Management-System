import mysql.connector
import pandas as pd
from cryptography.fernet import Fernet
import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import plotly.express as px

# Encryption key
key = b'xxTTd0bS9SR76fltNELEV5pJbRhKLfK0xEtSiBv0EgA='

# Connect to MySQL database
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

# Function to encrypt data using the key
def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# Function to decrypt encrypted data
def decrypt_data(encrypted_data, key):
    try:
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()
    except Exception as e:
        return None

def display_visualizations(decrypted_df):
    # Decrypt relevant columns
    decrypted_df 
    
    # Bar Plot for Departments
    st.subheader('Distribution of Students Across Departments')
    department_counts = decrypted_df['department'].value_counts()
    st.bar_chart(department_counts)

    
    
    st.subheader('CGPA in Department')
    cgpa_department = decrypted_df.groupby('department')['cgpa'].mean().reset_index()
    st.bar_chart(cgpa_department.set_index('department'))
    
    
    # Word Cloud for Father's Names
    st.subheader("Word Cloud of Father's Names")
    father_names = decrypted_df['father_name'].dropna().tolist()
    wordcloud_text = ' '.join(father_names)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wordcloud_text)
    st.image(wordcloud.to_array())

def visualizations_page(decrypted_df):
    if decrypted_df is not None and not decrypted_df.empty:
        # Display visualizations directly based on decrypted_df
        display_visualizations(decrypted_df)
    else:
        st.warning("No data to visualize.")

# Fetch encrypted data from the database
def fetch_encrypted_data(cursor):
    try:
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        st.error(f"Error fetching data from database: {e}")
        return []

# Insert data into the database
def insert_data(cursor, data):
    try:
        cursor.execute("""
            INSERT INTO students (id, roll_no, name, department, section, email, phone_number, address, cgpa, blood_group, father_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data)
    except mysql.connector.Error as e:
        st.error(f"Error inserting data into database: {e}")


def home():
    st.title("Accelerated Searchable Encrypted Database Management Systems for Cloud Services")

    st.header("Welcome to the AESDBMS Cloud Platform")

    st.markdown(
        """
        :cloud: **AESDBMS Cloud Platform**: Experience the power of secure and efficient database management in the cloud.
        """
    )

    st.header("Features")

    st.markdown(
        """
        - :closed_lock_with_key: **Encryption**: AESDBMS employs advanced encryption techniques to secure your data, preventing unauthorized access.
        - :mag_right: **Accelerated Search**: Our platform offers accelerated search capabilities, enabling fast and efficient data retrieval.
        - :chart_with_upwards_trend: **Scalability**: Easily scale your database infrastructure to accommodate growing data requirements.
        - :cloud: **Cloud Integration**: Seamlessly integrate AESDBMS with leading cloud service providers for flexible deployment options.
        - :floppy_disk: **Data Management**: Efficiently manage your data with comprehensive tools for storage, retrieval, and analysis.
        """
    )

    st.header("How to Get Started")

    st.markdown(
        """
        1. :bust_in_silhouette: **Sign Up**: Create an account on the AESDBMS Cloud Platform to get started.
        2. :gear: **Deploy Database**: Choose your preferred cloud service provider and deploy your encrypted database instance.
        3. :inbox_tray: **Insert Data**: Begin inserting your data securely into the encrypted database using AESDBMS's intuitive interface.
        4. :mag: **Accelerated Search**: Utilize our accelerated search feature to quickly retrieve the information you need.
        """
    )

    st.header("Security Measures")

    st.markdown(
        """
        - :key: **Encryption Key Management**: AESDBMS employs robust encryption key management techniques to safeguard your data.
        - :shield: **Access Control**: Granular access controls ensure that only authorized users can access sensitive data.
        - :bar_chart: **Regular Audits**: Regular security audits and monitoring mechanisms are in place to detect and prevent security threats.
        """
    )

    st.header("Future Enhancements")

    st.markdown(
        """
        - :robot: **Machine Learning Integration**: Integrate machine learning algorithms for predictive analysis and data-driven insights.
        - :link: **Blockchain Integration**: Explore the integration of blockchain technology for enhanced data integrity and transparency.
        - :chart_with_downwards_trend: **Advanced Analytics**: Enhance analytics capabilities for in-depth data analysis and visualization.
        """
    )

    st.header("About Us")

    st.markdown(
        """
        AESDBMS is developed by a team of experienced professionals dedicated to providing innovative database management solutions. 
        Our mission is to empower businesses with secure and efficient data management tools to drive growth and innovation.
        """
    )

    st.markdown(
        """
        For inquiries and support, please contact us at [support@aesdbms.com](mailto:support@aesdbms.com).
        """
    )

def insert_form(cursor):
    st.title("Insert Data into Database")

    st.write("Fill in the following fields to insert a new student record into the database.")

    st.header("Student Information")

    id = st.number_input("ID", min_value=1)
    roll_no = st.number_input("Roll No", min_value=1)
    name = st.text_input("Name")
    department = st.text_input("Department")
    section = st.text_input("Section")
    email = st.text_input("Email")
    phone_number = st.text_input("Phone Number")
    address = st.text_input("Address")
    cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, step=0.01)
    blood_group = st.text_input("Blood Group")
    father_name = st.text_input("Father's Name")

    st.header("Data Encryption")

    st.write("The entered data will be encrypted before being stored in the database for enhanced security.")

    if st.button("Insert Data"):
        # Encrypt the data
        encrypted_data = [
            id, roll_no, encrypt_data(name, key), encrypt_data(department, key),
            encrypt_data(section, key), encrypt_data(email, key), encrypt_data(phone_number, key),
            encrypt_data(address, key), cgpa, encrypt_data(blood_group, key), encrypt_data(father_name, key)
        ]

        # Insert the encrypted data into the database
        insert_data(cursor, encrypted_data)
        conn.commit()
        st.success("Data inserted successfully!")

    st.header("Note")

    st.write(
        """
        Ensure that all fields are filled correctly before inserting data. Once inserted, the data will be encrypted and stored securely in the database. 
        You can later search and retrieve this data using the search functionality provided.
        """
    )
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

# Search function
def search(cursor):
    st.title("Search Data")
    
    # Add some spacing for aesthetics
    st.write("")
    st.write("")
    
    # Add a header with a nice background color
    st.markdown("<h2 style='text-align: center; color: white; background-color: #68a0cf; padding: 10px;'>Search Data</h2>", unsafe_allow_html=True)
    
    # Text input box with a placeholder and some padding
    search_term = st.text_input("Search (substring)", placeholder="Enter search term...", key="search_input").strip()
    
    # Add some spacing for aesthetics
    st.write("")
    
    if st.button("Search"):
        # Fetch encrypted data
        encrypted_data = fetch_encrypted_data(cursor)
        
        if encrypted_data:
            # Decrypt data and filter based on search term
            filtered_data = []
            for record in encrypted_data:
                decrypted_record = [decrypt_data(field, key) if isinstance(field, str) else field for field in record]
                if any(search_term.lower() in str(field).lower() for field in decrypted_record):
                    filtered_data.append(decrypted_record)

            if filtered_data:
                headers = [i[0] for i in cursor.description]  # Fetch column names from cursor description
                
                # Add some spacing for aesthetics
                st.write("")
                st.subheader("Search Results:")
                
                # Add custom CSS to style the table
                st.markdown(
                    f"""
                    <style>
                    table {{border-collapse: collapse; width: 100%;}}
                    th, td {{padding: 8px; text-align: left; border-bottom: 1px solid #ddd;}}
                    th {{background-color: #f2f2f2;}}
                    </style>
                    """, unsafe_allow_html=True
                )
                
                # Display the filtered data in a nice table
                st.table(pd.DataFrame(filtered_data, columns=headers))
            else:
                st.info("No matching records found.")
        else:
            st.warning("No encrypted data found in the database.")

def fetch_encrypted_data(cursor):
    try:
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        st.error(f"Error fetching data from database: {e}")
        return []
def display_encrypted_database(cursor):
    st.title("Encrypted Database")

    st.write("Below is the encrypted database stored in the MySQL database:")
    
    st.write("This table displays the encrypted student records.")
    st.write("To view decrypted data, please use the 'Full Data' page.")

    # Fetch encrypted data
    encrypted_data = fetch_encrypted_data(cursor)
    if encrypted_data:
        headers = [i[0] for i in cursor.description] 
        st.table(pd.DataFrame(encrypted_data, columns=headers))
    else:
        st.warning("No encrypted data found in the database.")

# Full data display
def full_data(cursor):
    st.title("Full Data")
    # Fetch encrypted data
    encrypted_data = fetch_encrypted_data(cursor)
    if encrypted_data:
        headers = [i[0] for i in cursor.description]  
        st.subheader("Full Data:")
        # Decrypt all data
        decrypted_data = []
        for record in encrypted_data:
            decrypted_record = [decrypt_data(field, key) if isinstance(field, str) else field for field in record]
            decrypted_data.append(decrypted_record)
        # Create a DataFrame from decrypted data
        decrypted_df = pd.DataFrame(decrypted_data, columns=headers)
        # Display the DataFrame using Streamlit table
        st.table(decrypted_df)
        return decrypted_df
    else:
        st.warning("No encrypted data found in the database.")
        return None  # Return None if no data is found

# Streamlit App
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Insert Data", "Search", "Full Data", "Encrypted Database", "Visualizations"])

    # MySQL database connection parameters
    host = 'localhost'
    username = 'root'
    password = ''
    database = 'student_database'

    # Connect to the database
    conn, cursor = connect_to_database(host, username, password, database)

    if page == "Home":
        home()
    elif page == "Insert Data":
        if conn:
            insert_form(cursor)
        else:
            st.error("Failed to connect to MySQL database.")
    elif page == "Search":
        if conn:
            search(cursor)
        else:
            st.error("Failed to connect to MySQL database.")
    elif page == "Full Data":
        if conn:
            full_data(cursor)
        else:
            st.error("Failed to connect to MySQL database.")
    elif page == "Encrypted Database":
        if conn:
            display_encrypted_database(cursor)
    elif page == "Visualizations":
        if conn:
            decrypted_df = full_data(cursor)  
            visualizations_page(decrypted_df)  
        else:
            st.error("Failed to connect to MySQL database.")
    else:
        st.error("Failed to connect to MySQL database.")
    

    # Close database connection
    if conn:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

 # Secure Cloud Database Management System (AESDBMS)
**Accelerated Searchable Encrypted Database Management System — Streamlit + MySQL**

This repository demonstrates a secure, searchable database with **field-level encryption** using **Fernet** (from `cryptography`), **MySQL** for storage, and a **Streamlit** web UI for inserting records, searching (client-side), viewing full decrypted data, and visualizing basic insights.

> ⚠️ Educational demo. Not production-ready. Add auth, secret management, KMS, auditing, and role-based access before real deployments.

---

## ✨ Key Features
- 🔐 **Field-level encryption** of sensitive text (name, email, phone, etc.) using Fernet; ciphertext stored in MySQL `TEXT` columns.
- 🔎 **Accelerated (client-side) search** against decrypted rows in memory.
- 📊 **Visualizations**: students by department, average CGPA per department, and a word cloud of father names.
- 🧪 **Ad-hoc SQL (local only)**: run SELECT queries; results are decrypted for display.

---

## 🧱 Architecture (as implemented)
Streamlit (UI) ──> mysql-connector-python ──> MySQL (ciphertext at rest)
↑ │
└─────── Decrypt in app (Fernet) ◄──────┘

pgsql
Copy code
- **Encrypt on insert**, store ciphertext in MySQL.
- **Fetch + decrypt in memory** for display/search.
- Searching is **not** over ciphertext; it’s over the **decrypted** rows within the app session.

### Mapping to the paper’s components
| Paper Module | This Repo (Minimal Implementation) |
| --- | --- |
| UI / Web Browser | Streamlit pages (Home, Insert, Search, Full Data, Encrypted Database, Visualizations, Execute Query) |
| Backend Services | Python functions for encryption/decryption, inserts, selects |
| Encryption Module | Fernet (symmetric) via `cryptography` |
| DBMS | MySQL 8.x (local) |
| Security Layer | Field encryption + local dev only (no auth yet) |

**Project context & alignment:** The document *“Secure Cloud Database Management System / AESDBMS Cloud Platform”* details architecture, security goals, cloud integration, and future work. This repo implements a **student records** demo of those ideas and can be extended to the paper’s healthcare/other domains. :contentReference[oaicite:0]{index=0}

---

## 📂 Repository Structure
.
├── test.py # Streamlit app (all pages)
├── student_database.sql # Schema/seed file (import via Workbench/CLI)
├── requirements.txt # Python dependencies
└── README.md # This file

markdown
Copy code

**requirements.txt**
streamlit
mysql-connector-python
cryptography
pandas
wordcloud
plotly
python-dotenv

yaml
Copy code

---

## 🛠️ Prerequisites
- **Python 3.10+**
- **MySQL 8.x** (running locally; MySQL Workbench recommended)
- (Optional) **XAMPP/phpMyAdmin** as an alternative MySQL GUI (not required if using Workbench)

---

## 🗄️ Database Setup
### 1) Import schema
**Workbench (GUI)**  
`Server → Data Import → Import from Self-Contained File → student_database.sql → Target schema: student_database → Start Import`  
If you don’t see it in the left panel, right-click **SCHEMAS** → **Refresh All**.

**CLI (alt.)**
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS student_database;"
mysql -u root -p student_database < student_database.sql
2) Resize columns for encryption (important)
Fernet tokens are long. Ensure encrypted columns are TEXT:

sql
Copy code
USE student_database;
ALTER TABLE students
  MODIFY name TEXT,
  MODIFY department TEXT,
  MODIFY section TEXT,
  MODIFY email TEXT,
  MODIFY phone_number TEXT,
  MODIFY address TEXT,
  MODIFY blood_group TEXT,
  MODIFY father_name TEXT;
3) Table reference
Column	Type	Encrypted?
id	INT (PK)	❌
roll_no	INT	❌
name	TEXT	✅
department	TEXT	✅
section	TEXT	✅
email	TEXT	✅
phone_number	TEXT	✅
address	TEXT	✅
cgpa	DECIMAL(3,2)	❌
blood_group	TEXT	✅
father_name	TEXT	✅

▶️ Run the App
1) Create & activate a virtual environment
Windows (PowerShell)

powershell
Copy code
# Path may contain spaces — quote it
cd "C:\Users\<you>\Desktop\secure cloud database"
python -m venv .venv
.\.venv\Scripts\Activate
If you get a script policy error:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

macOS / Linux

bash
Copy code
cd /path/to/your/project
python3 -m venv .venv
source .venv/bin/activate
2) Install dependencies
bash
Copy code
pip install -r requirements.txt
# or:
pip install streamlit mysql-connector-python cryptography pandas wordcloud plotly python-dotenv
3) Configure credentials & key (test.py)
python
Copy code
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "<YOUR_MYSQL_PASSWORD>"
DB_NAME = "student_database"
Generate a Fernet key once and paste it:

python
Copy code
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
# In test.py:
key = b'PASTE_THE_BASE64_KEY_HERE'
Keep the key stable. Changing it later will prevent old rows from decrypting.

(Optional) Use a .env:

ini
Copy code
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=<YOUR_MYSQL_PASSWORD>
MYSQL_DB=student_database
FERNET_KEY=<BASE64_KEY_NO_QUOTES>
Load in code:

python
Copy code
from dotenv import load_dotenv; import os
load_dotenv()
DB_HOST = os.getenv("MYSQL_HOST","localhost")
DB_USER = os.getenv("MYSQL_USER","root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD","")
DB_NAME = os.getenv("MYSQL_DB","student_database")
key = os.getenv("FERNET_KEY").encode()
4) Launch Streamlit
bash
Copy code
streamlit run test.py
Open the URL (usually http://localhost:8501).

🧭 App Pages
Home — overview.

Insert Data — encrypt + insert new rows.

Search — client-side substring search over decrypted data.

Full Data — full decrypted table.

Encrypted Database — raw ciphertext.

Visualizations — dept distribution, avg CGPA per dept, father-name word cloud.

Execute Query — run custom SQL (local/dev only).

🔐 Security Notes
Secrets: prefer env vars or a secrets manager; do not commit keys.

Local demo only: add auth, RBAC, TLS, and KMS for keys in real deployments.

“Execute Query” allows arbitrary SQL; remove/lock down for shared environments.

🧪 Handy SQL (Workbench/CLI)
sql
Copy code
SHOW DATABASES;
USE student_database;
DESCRIBE students;
SELECT * FROM students LIMIT 5;
🚧 Troubleshooting
Don’t see student_database in Workbench → Right-click SCHEMAS → Refresh All; check the filter icon.

Access denied/auth plugin → Verify credentials. If needed:

sql
Copy code
ALTER USER 'root'@'localhost'
  IDENTIFIED WITH mysql_native_password BY '<YourPassword>';
FLUSH PRIVILEGES;
Data too long for column → Run the ALTER TABLE ... TEXT migration above.

Decryption fails/gibberish → The Fernet key changed after inserts. Use the original key or reinsert with the new key.

streamlit not found → Activate your venv and reinstall deps.

🧭 Future Work (from the paper)
ML-assisted analytics, anomaly detection, trend forecasting

Blockchain for integrity/auditability

Cloud provider SDK integrations (AWS/GCP/Azure), KMS-backed keys

Federated learning, collaborative analytics

Monitoring, auditing, and compliance (HIPAA/GDPR) foundations


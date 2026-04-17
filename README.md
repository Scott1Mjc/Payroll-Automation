# Payroll Automation

Automates the process of splitting, organizing, and sending payroll (holerite) PDFs to employees via email.

This project was built to eliminate repetitive manual work in HR routines, reducing errors and saving time.

---

## Features

* Upload a full payroll PDF
* Automatically split by employee
* Intelligent name detection from documents
* Organized folder structure by year/month/employee
* Employee email management
* Bulk email sending with attachments
* Encrypted storage of email credentials
* Custom email signature (image or HTML)

---

## Project Structure

```
Payroll Automation/
├── app.py                  # Main entrypoint
├── requirements.txt
├── .gitignore
├── core/
│   ├── constants.py        # Constants and mappings
│   ├── crypto.py           # Password encryption
│   ├── storage.py          # JSON read/write
│   ├── pdf_processor.py    # PDF splitting and saving
│   └── email_sender.py     # Sending via Gmail API
├── ui/
│   ├── sidebar.py          # Employee sidebar
│   ├── tab_split.py        # Tab 1 — Split PDF
│   ├── tab_email.py        # Tab 2 — Send Emails
│   └── tab_files.py        # Tab 3 — Generated Files
└── utils/
    └── string_helpers.py   # String helper functions
```

---

## Technologies Used

* Python
* Streamlit
* PyMuPDF (fitz)
* Pandas
* SMTP (Gmail)
* Cryptography (Fernet)

---

## Installation

```bash
git clone https://github.com/Scott1Mjc/Payroll-Automation
cd Payroll-Automation
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

---

## 📌 How It Works

1. Upload a payroll PDF file
2. The system identifies each employee
3. Splits the file into individual PDFs
4. Organizes files into folders:

   ```
   Payrrolls / Year / Month / Employee / Type
   ```
5. Sends emails automatically with attachments

---

## 🔐 Security

* Email credentials are stored using encryption (Fernet)
* Sensitive files are ignored via `.gitignore`

---

## ⚠️ Notes

* Designed to work with Brazilian payroll (holerite) layouts
* Name detection depends on document formatting
* Gmail requires an **App Password** for SMTP

---

## 👨‍💻 Author

Developed for automating HR workflows and improving operational efficiency.

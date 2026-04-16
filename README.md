# Payrroll Automation

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
payrroll-automation/
│
├── app.py
├── core/
├── utils/
├── data/
├── assets/
└── output/
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
git clone https://github.com/Scott1Mjc/Payrroll-Automation
cd Payrroll-Automation
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

## 💡 Future Improvements

* API version (FastAPI)
* Database integration
* Cloud storage (S3 / Azure Blob)
* Better PDF layout detection (AI / OCR)

---

## 👨‍💻 Author

Developed for automating HR workflows and improving operational efficiency.

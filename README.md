# 📨 Visa Automation Bot (Python)

This project is a Python-based intelligent agent designed to automate the creation and delivery of visa support letters for a Human Resources Department. It monitors a folder for incoming JSON files, generates letters using a Word document template, and simulates email delivery by logging the output.

---

## 💡 What It Does

1. Watches the `uploads/` folder for new or modified `.json` files
2. Extracts user data like `name`, `nationality`, and `start_date`
3. Renders a visa support letter from a `.docx` template using that data
4. Simulates sending an email by logging the message to a `.txt` file

---

## 📁 Folder Structure

```
visa_bot.py             → main automation script
visa_template.docx      → DOCX template using Jinja2-style {{ variables }}
uploads/                → input folder for .json files
sent_emails/            → output folder for simulated email logs
```

---

## 🧪 Example Input

File: `uploads/carlos_test.json`

```json
{
  "name": "Carlos Test",
  "nationality": "Chilean",
  "start_date": "May 10, 2025",
  "email": "carlos@mail.tm"
}
```

---

## 📤 Simulated Output

```
📤 Simulated Temp Email Sent:
To: carlos@mail.tm
Subject: Your Visa Support Letter
Attachment: visa_letter_carlos_test.docx
📝 Email log saved to sent_emails/email_to_carlos_at_mail.tm.txt
```

---

## 🚀 Run It

Make sure your terminal is in the project directory:

```bash
python visa_bot.py
```

Then drop or modify a `.json` file inside the `uploads/` folder to trigger the process.

---

## 🔧 Requirements

Install dependencies:

```bash
pip install docxtpl watchdog
```

---

## 📦 Recommended .gitignore

```
__pycache__/
sent_emails/
*.log
```

---

## 🎓 Built For

Course: **Intelligent Agents & Process Automation**  
Project: **Visa Automation Demo**  
Author: **Felipe Rojas**


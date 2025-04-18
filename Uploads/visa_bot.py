import os
import time
import json
from docxtpl import DocxTemplate
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === SETTINGS ===
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")

# === Watcher Class ===
class UploadHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"🔍 Event detected: {event.event_type} - {event.src_path}")

    def on_created(self, event):
        print(f"📁 Change detected: {event.src_path}")
        if event.is_directory:
            print(f"📂 Ignored directory creation: {event.src_path}")
            return
        if event.src_path.endswith(".json"):
            print(f"📥 New file detected: {event.src_path}")
            try:
                if not os.path.exists(event.src_path):
                    print(f"❌ File does not exist: {event.src_path}")
                    return
                if not os.access(event.src_path, os.R_OK):
                    print(f"❌ File is not readable: {event.src_path}")
                    return
                process_file(event.src_path)
            except Exception as e:
                print(f"❌ Error in on_created: {e}")
        else:
            print(f"⚠️ Ignored non-JSON file: {event.src_path}")

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".json"):
            print(f"✏️ Modified file detected: {event.src_path}")
            try:
                if os.path.exists(event.src_path) and os.access(event.src_path, os.R_OK):
                    process_file(event.src_path)
            except Exception as e:
                print(f"❌ Error in on_modified: {e}")

# === Process New JSON File ===
def process_file(filepath):
    try:
        print(f"🔄 Processing file: {filepath}")
        with open(filepath, 'r') as file:
            data = json.load(file)

        template_path = os.path.join(os.path.dirname(__file__), "visa_template.docx")
        print(f"📄 Using template at: {template_path}")
        template = DocxTemplate(template_path)
        template.render(data)  # <-- THE FIX: render the template with data

        output_filename = os.path.join(UPLOADS_DIR, f"visa_letter_{data['name'].lower().replace(' ', '_')}.docx")
        template.save(output_filename)
        print(f"✅ Visa letter generated: {output_filename}")

        send_temp_email(data['email'], output_filename)
    except Exception as e:
        print(f"❌ Error processing file {filepath}: {e}")

# === Simulate Sending to Temp Email ===
def send_temp_email(recipient_email, attachment):
    print(f"📤 Preparing to send email to: {recipient_email}")
    print(f"""
📤 Simulated Temp Email Sent:
To: {recipient_email}
Subject: Your Visa Support Letter
Body: Please find attached your visa support letter.
Attachment: {attachment}
""")
    try:
        os.makedirs("sent_emails", exist_ok=True)
        email_log = os.path.join("sent_emails", f"email_to_{recipient_email.replace('@', '_at_')}.txt")
        with open(email_log, "w") as f:
            f.write(f"TO: {recipient_email}\nSUBJECT: Visa Support Letter\nATTACHMENT: {attachment}\n")
        print(f"📝 Email log saved to {email_log}\n")
    except Exception as e:
        print(f"❌ Error saving email log: {e}")

# === Main Watcher ===
if __name__ == "__main__":
    print(f"👀 Monitoring folder: {os.path.abspath(UPLOADS_DIR)}/")
    os.makedirs(UPLOADS_DIR, exist_ok=True)

    print(f"📂 Initial files in {UPLOADS_DIR}: {os.listdir(UPLOADS_DIR)}")

    event_handler = UploadHandler()
    observer = Observer()
    observer.schedule(event_handler, UPLOADS_DIR, recursive=False)
    observer.start()

    test_file = os.path.join(UPLOADS_DIR, "carlos_test.json")
    if os.path.exists(test_file):
        print(f"🔧 Manually processing file: {test_file}")
        process_file(test_file)
    else:
        print(f"❌ Test file not found: {test_file}")

    try:
        while True:
            print("🔄 Waiting for new files...")
            print(f"📂 Current files in {UPLOADS_DIR}: {os.listdir(UPLOADS_DIR)}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("🛑 Stopping observer...")
        observer.stop()
    observer.join()

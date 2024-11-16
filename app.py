import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import subprocess
from pathlib import Path
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Directory to temporarily store downloaded videos
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Get the absolute path to the current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Specify the path to yt-dlp.exe
coder_path = os.path.join(BASE_DIR, 'yt-dlp.exe')

def download_video(url):
    try:
        # Generate a unique filename to avoid conflicts
        unique_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")
        
        # Construct the yt-dlp command
        command = [coder_path, url, '-o', output_template]
        print(f"Executing command: {' '.join(command)}")
        
        # Run the command using subprocess
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            flash("Video downloaded successfully.", "success")
            
            # Find the downloaded file
            downloaded_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(unique_id)]
            if downloaded_files:
                return downloaded_files[0]  # Return the first matching file
            else:
                raise FileNotFoundError("Downloaded file not found.")
        else:
            flash(f"An error occurred: {result.stderr}", "error")
            print(f"Error: {result.stderr}")
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        print(f"Exception: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    # Remove extra parameters like &t= from the URL
    if '&' in url:
        url = url.split('&')[0]
    
    downloaded_file = download_video(url)
    if downloaded_file:
        return redirect(url_for('serve_file', filename=downloaded_file))
    return redirect(url_for('index'))

@app.route('/downloads/<filename>')
def serve_file(filename):
    # Serve the file to the user
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


'''
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import yt_dlp
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Define a temporary folder for storing downloaded videos
TEMP_FOLDER = 'temp_downloads'
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

def download_video(url):
    try:
        unique_filename = f"{uuid.uuid4()}.%(ext)s"
        output_path = os.path.join(TEMP_FOLDER, unique_filename)

        ydl_opts = {
            'outtmpl': output_path,
            'cookiefile': 'cookies.txt',  # Use YouTube cookies for authentication
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        flash("Video downloaded successfully. Ready for download.", "success")
        return output_path.rsplit('/', 1)[-1]
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    if '&' in url:
        url = url.split('&')[0]

    downloaded_file = download_video(url)
    if downloaded_file:
        return redirect(url_for('serve_file', filename=downloaded_file))
    return redirect(url_for('index'))

@app.route('/serve/<filename>')
def serve_file(filename):
    try:
        return send_from_directory(TEMP_FOLDER, filename, as_attachment=True)
    except Exception as e:
        flash(f"Error serving file: {e}", "error")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
'''

'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import yt_dlp
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def download_video(url):
    try:
        flash("Turn Off VPN")
        with yt_dlp.YoutubeDL() as ydl:  # No options specified
            ydl.download([url])
        flash("Video downloaded successfully.", "success")
    except Exception as e:
        flash(f"An error occurred: {e}", "error")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    # Try removing the &t= part of the URL if present
    if '&' in url:
        url = url.split('&')[0]
    download_video(url)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
'''
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import uuid
import subprocess
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_key')  # Use an environment variable for the secret key

# Directory to temporarily store downloaded videos
DOWNLOAD_DIR = "downloads"
try:
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
except OSError as e:
    logger.error(f"Error creating directory {DOWNLOAD_DIR}: {e}")
    raise

# Path to yt_dlp.exe
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
YTDLP_PATH = os.path.join(BASE_DIR, 'yt_dlp.exe')  # Ensure yt_dlp.exe is in the same directory as this script

def download_video(url):
    """Download video using yt_dlp.exe and return the filename."""
    try:
        # Generate a unique filename to avoid conflicts
        unique_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")
        
        # Construct the yt-dlp command
        command = [YTDLP_PATH, url, '-o', output_template]
        logger.info(f"Executing command: {' '.join(command)}")
        
        # Run the command using subprocess
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("Video downloaded successfully.")
            flash("Video downloaded successfully.", "success")
            
            # Find the downloaded file
            downloaded_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(unique_id)]
            if downloaded_files:
                return downloaded_files[0]  # Return the first matching file
            else:
                raise FileNotFoundError("Downloaded file not found.")
        else:
            logger.error(f"yt-dlp error: {result.stderr}")
            flash(f"An error occurred: {result.stderr}", "error")
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        logger.error(f"Exception during video download: {e}")
        return None

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    """Handle video download requests."""
    url = request.form['url']
    # Sanitize URL by removing extra parameters
    if '&' in url:
        url = url.split('&')[0]
    
    downloaded_file = download_video(url)
    if downloaded_file:
        return redirect(url_for('serve_file', filename=downloaded_file))
    return redirect(url_for('index'))

@app.route('/downloads/<filename>')
def serve_file(filename):
    """Serve the downloaded file to the user."""
    try:
        return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        flash("File not found.", "error")
        logger.error(f"File not found: {filename}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)  # Set debug to False for production



'''
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import uuid
import subprocess
from pathlib import Path

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

'''
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from yt_dlp import YoutubeDL
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Directory to temporarily store downloaded videos
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Path to cookies file
COOKIES_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "cookies.txt")

def download_video(url):
    try:
        # Generate a unique filename to avoid conflicts
        unique_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")

        # yt-dlp options
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'cookiefile': COOKIES_FILE,  # Add cookies file
        }

        # Use yt-dlp to download the video
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the downloaded file
        downloaded_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(unique_id)]
        if downloaded_files:
            return downloaded_files[0]  # Return the first matching file
        else:
            raise FileNotFoundError("Downloaded file not found.")
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
'''
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from yt_dlp import YoutubeDL
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Directory to temporarily store downloaded videos
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video(url):
    try:
        # Generate a unique filename to avoid conflicts
        unique_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")

        # yt-dlp options
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
        }

        # Use yt-dlp to download the video
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the downloaded file
        downloaded_files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(unique_id)]
        if downloaded_files:
            return downloaded_files[0]  # Return the first matching file
        else:
            raise FileNotFoundError("Downloaded file not found.")
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



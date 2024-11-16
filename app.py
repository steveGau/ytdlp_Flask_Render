from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import uuid
import subprocess
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

# Path to yt-dlp binary (Linux version)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
YTDLP_PATH = os.path.join(BASE_DIR, 'yt-dlp')  # Ensure yt-dlp is in the same directory

def download_video(url):
    """Download video using yt-dlp binary and return the filename."""
    try:
        # Generate a unique filename to avoid conflicts
        unique_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f"{unique_id}.%(ext)s")
        
        # Path to cookies file
        cookies_file = os.path.join(BASE_DIR, 'cookies.txt')
        
        # Construct the yt-dlp command
        command = [
            YTDLP_PATH,
            '--cookies', cookies_file,
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            url,
            '-o', output_template
        ]
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

# Path to yt-dlp binary (Linux version)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
YTDLP_PATH = os.path.join(BASE_DIR, 'yt-dlp')  # Ensure yt-dlp is in the same directory

def download_video(url):
    """Download video using yt-dlp binary and return the filename."""
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
''
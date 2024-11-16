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
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import yt_dlp
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def download_video(url):
    try:
        ydl_opts = {
            'outtmpl': 'downloadVideos/%(title)s.%(ext)s',
            'verbose': True,  # Enable verbose output
        }
        # Create 'downloadVideos' directory if it doesn't exist
        if not os.path.exists('downloadVideos'):
            os.makedirs('downloadVideos')
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
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

from flask import Flask, render_template, request, redirect, url_for, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def download_video(url):
    try:
        ydl_opts = {
            'outtmpl': 'downloadVideos/%(title)s.%(ext)s',
            'verbose': True,  # Enable verbose output
            'cookiefile': 'C:/Users/a2907/AppData/Local/Google/Chrome/User Data/Default/Network/Cookies',
            'proxy': 'http://your.proxy.address:port'
        }
        ```[_{{{CITATION{{{_2{ERROR: [youtube] ZkW3aoYhFwY: Sign in to confirm you’re not a bot. This ...](https://github.com/yt-dlp/yt-dlp/issues/10683)

       
        # Create 'downloadVideos' directory if it doesn't exist
        if not os.path.exists('downloadVideos'):
            os.makedirs('downloadVideos')
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
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
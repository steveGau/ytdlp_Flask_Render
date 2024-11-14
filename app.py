from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def download_video(url):
    try:
        coder_path ='yt-dlp.exe '
        best=' -f bv*+ba '
        best=' '
        youtube=coder_path+best
        print(youtube+url)
        print(os.path.abspath(coder_path + best))
        # Create 'downloadVideos' directory if it doesn't exist
        if not os.path.exists('downloadVideos'):
            os.makedirs('downloadVideos')   
        subprocess.run(youtube+url, shell=True)  # Execute the line using subprocess
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

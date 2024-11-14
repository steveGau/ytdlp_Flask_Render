from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def download_video(url):
    try:
        coder_path = 'yt-dlp '
        best = ' -f bv*+ba '
        best = ' '
        youtube = coder_path + best
        print(youtube + url)
        
        # Get the default Downloads directory for the current user
        target_dir = str(Path.home() / "Downloads")

        # Construct the full command with the output directory
        # command = youtube + url + f' -o {target_dir}/%(title)s.%(ext)s'
        command = youtube + url + f' -o {target_dir}/%(title)s.%(ext)s'        
        print(f'Executing command: {command}')
        
        # Run the command using subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            flash("Video downloaded successfully.", "success")
            # Print the directory where the video is downloaded
            flash(f"Video is saved in: {os.path.abspath(target_dir)}")
            # flash(f"Video is saved in: {os.path.abspath(target_dir)}", "info")
            # print(f"Video is saved in: {os.path.abspath(target_dir)}")
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
    # Try removing the &t= part of the URL if present
    if '&' in url:
        url = url.split('&')[0]
    download_video(url)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def download_video(url):
    try:
        coder_path = 'yt-dlp '
        best = ' -f bv*+ba '
        best = ' '
        youtube = coder_path + best
        print(youtube + url)
        
        # Get the default Downloads directory for the current user
        download_dir = str(Path.home() / "Downloads")
        
        # Create 'downloadVideos' directory within Downloads if it doesn't exist
        target_dir = os.path.join(download_dir, 'downloadVideos')
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        
        # Construct the full command with the output directory
        command = youtube + url + f' -o {target_dir}/%(title)s.%(ext)s'
        print(f'Executing command: {command}')
        
        # Run the command using subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            flash("Video downloaded successfully.", "success")
            
            # Print the directory where the video is downloaded
            flash(f"Video is saved in: {os.path.abspath(target_dir)}", "info")
            print(f"Video is saved in: {os.path.abspath(target_dir)}")
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
    # Try removing the &t= part of the URL if present
    if '&' in url:
        url = url.split('&')[0]
    download_video(url)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
'''

'''
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def download_video(url):
    try:
        # coder_path ='yt-dlp.exe '
        coder_path ='yt-dlp '
        best=' -f bv*+ba '
        best=' '
        youtube=coder_path+best
        print(youtube+url)
        print(os.path.abspath(coder_path + best))
        # Create 'downloadVideos' directory if it doesn't exist
        # if not os.path.exists('downloadVideos'):
        #     os.makedirs('downloadVideos')   
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
'''
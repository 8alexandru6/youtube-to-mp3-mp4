from flask import Flask, render_template, request, send_file, redirect, url_for
#from pytube import YouTube # Remove the original pytube import
from pytubefix import YouTube # Import pytubefix
from pytubefix.cli import on_progress # Import on_progress
import os

print("Starting the Flask app...") # Add this line
app = Flask(__name__)
print("Flask app created") #Add this line
app.config['UPLOAD_FOLDER'] = 'downloads'  # Folder to save downloaded files

# Ensure the downloads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
print("Upload folder created") # Add this line

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        format_choice = request.form.get("format_choice")  # Get the format choice

        try:
            print(f"Attempting to download: {youtube_url}")
            yt = YouTube(youtube_url, on_progress_callback=on_progress)
            print(f"Video Title: {yt.title}")

            if format_choice == "mp3":
                # Download as MP3 (audio only)
                stream = yt.streams.filter(only_audio=True).first()
                if stream:
                    filename = yt.title.replace(" ", "_") + ".mp3"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    print(f"Downloading to: {filepath}")
                    stream.download(output_path=app.config['UPLOAD_FOLDER'], filename=filename)
                    return send_file(filepath, as_attachment=True, download_name=filename)
                else:
                    return "Error: No audio stream found."

            elif format_choice == "mp4":
                # Download as MP4 (video with audio)
                stream = yt.streams.get_highest_resolution() #Get highest resolution
                if stream:
                    filename = yt.title.replace(" ", "_") + ".mp4"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    print(f"Downloading to: {filepath}")
                    stream.download(output_path=app.config['UPLOAD_FOLDER'], filename=filename)
                    return send_file(filepath, as_attachment=True, download_name=filename)
                else:
                    return "Error: No video stream found."

            else:
                return "Error: Please select a format (MP3 or MP4)."

        except Exception as e:
            print(f"An error occurred: {e}")
            return f"Error: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    print("Running the app...") # Add this line
    app.run(debug=True)  # debug=True for development, remove in production
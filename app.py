from flask import Flask, render_template, request, send_file, redirect, url_for
from pytubefix import YouTube 
from pytubefix.cli import on_progress 
import os

print("Starting the Flask app...") 
app = Flask(__name__)
print("Flask app created") 
app.config['UPLOAD_FOLDER'] = 'downloads' 

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
print("Upload folder created") 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        format_choice = request.form.get("format_choice")

        try:
            print(f"Attempting to download: {youtube_url}")
            yt = YouTube(youtube_url, on_progress_callback=on_progress)
            print(f"Video Title: {yt.title}")

            if format_choice == "mp3":
                audio_quality = request.form.get("audio_quality", "best")  # Get audio quality preference
                if audio_quality == "best":
                    stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first() #Get highest bitrate
                elif audio_quality == "low":
                     stream = yt.streams.filter(only_audio=True).order_by('abr').asc().first() #Get lowest bitrate
                else:
                    return "Invalid audio quality selection."

                if stream:
                    filename = yt.title.replace(" ", "_") + ".mp3"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    print(f"Downloading to: {filepath}")
                    stream.download(output_path=app.config['UPLOAD_FOLDER'], filename=filename)
                    return send_file(filepath, as_attachment=True, download_name=filename)
                else:
                    return "Error: No audio stream found."

            elif format_choice == "mp4":
                video_quality = request.form.get("video_quality", "highest") # Get video quality preference
                if video_quality == "highest":
                    stream = yt.streams.get_highest_resolution()
                elif video_quality == "lowest":
                    stream = yt.streams.get_lowest_resolution()
                else:
                    return "Invalid video quality selection."

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
    print("Running the app...")
    app.run(debug=True)

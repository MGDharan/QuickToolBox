import os
from pytube import YouTube
import instaloader
import yt_dlp
from docx2pdf import convert

# Function for downloading Instagram posts and reels
def download_instagram(url, download_dir):
    try:
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_url(loader.context, url)
        loader.download_post(post, target=download_dir)
        return f"Downloaded Instagram post: {post.title}"
    except Exception as e:
        return f"Error downloading Instagram post: {str(e)}"

# Function for downloading YouTube videos
def download_youtube_video(url, download_dir):
    try:
        # Remove query parameters to ensure valid URL
        clean_url = url.split('?')[0]
        
        yt = YouTube(clean_url)
        stream = yt.streams.get_highest_resolution()
        stream.download(download_dir)
        return f"Downloaded video: {yt.title}"
    except Exception as e:
        # If pytube fails, try using yt-dlp
        try:
            ydl_opts = {
                'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
                'format': 'best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return "Downloaded successfully using yt-dlp!"
        except Exception as e:
            return f"Error downloading video: {str(e)}"

# Function for converting Word documents to PDF
def word_to_pdf(input_path, output_path):
    try:
        convert(input_path, output_path)
        return f"Word document successfully converted to PDF at {output_path}"
    except Exception as e:
        return f"Error converting Word document: {str(e)}"

# Main execution flow
def main():
    download_dir = "downloads"  # Ensure this folder exists, or create it
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    print("Choose an option:")
    print("1. Instagram Post/Video Downloader")
    print("2. YouTube Video Downloader")
    print("3. Word to PDF Converter")
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        instagram_url = input("Enter Instagram Post URL: ")
        print(download_instagram(instagram_url, download_dir))

    elif choice == "2":
        youtube_url = input("Enter YouTube Video URL: ")
        print(download_youtube_video(youtube_url, download_dir))

    elif choice == "3":
        word_file = input("Enter the path to the Word document: ")
        output_pdf = input("Enter the path where you want to save the PDF: ")
        print(word_to_pdf(word_file, output_pdf))

    else:
        print("Invalid choice. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()

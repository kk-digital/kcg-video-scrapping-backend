# Setup Guide for Application

## Install prerequisites

```
sudo apt update
sudo apt install -y python3-pip
sudo apt install -y python3-venv
```

## Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies

```
pip3 install -r requirements.txt
```

## Install mongodb on ubuntu

sudo apt update
sudo apt install -y gnupg curl
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
mongod --version

## Run the application

```
dotenv -f  .env run  uvicorn main:app --reload --port 9000
```

# Preference 

## Setup yt-dlp library

### Oauth2 for extracting video metadata and downloading video

- install yt-dlp library

```
pip3 install yt-dlp==2024.10.22
pip3 install yt-dlp-youtube-oauth2
```

- Initialize the OAuth2 Authorization(Optional)

```
yt-dlp --username oauth2 --password "" https://www.youtube.com/watch?v=6_rFbDToh8w
```

- Add token data as token_data.json in youtube-oauth2 of cache

```
cd ~/.cache/yt-dlp/youtube-oauth2
```

- To give yt-dlp access to your account, go to  https://www.google.com/device  and enter code in description
- Add username and password to config

### Cookie for extracting video metadata and downloading videos

- [Exporting YouTube cookies](https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies)

    If you are unfamiliar with the basics of exporting cookies and passing them to yt-dlp, then first see [How do I pass cookies to yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)

    YouTube rotates cookies frequently on open YouTube browser tabs as a security measure. To export cookies that will remain working with yt-dlp, you will need to export cookies in such a way that they are never rotated.

    One way to do this is through a private browsing/incognito window:

    1. Open a new private browsing/incognito window and log into YouTube
    2. Open a new tab and close the YouTube tab
    3. Export cookies from the browser then close the private browsing/incognito window so the session is never opened in the browser again.

- Add cookie to yt-dlp config as follows:

    ```
    ydl_opts = {
        "format": "bv[height=720][fps=60]/bv[height=720][fps=30]", # specific file format
        "cookiefile": "cookies.txt", # cookie file path
        "http_headers": {  
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        "outtmpl": "%(title)s.%(ext)s", # download file name format
    }
    ```
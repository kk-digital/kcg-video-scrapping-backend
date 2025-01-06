# Install mongodb on ubuntu

sudo apt update
sudo apt install -y gnupg curl
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
mongod --version

# Oauth2 for extracting video metadata and downloading video

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

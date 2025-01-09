
import re

def get_youtube_video_id(url):
    '''
    Extract short hash form youtube video url
    '''
    # Regular expression to match YouTube video URLs
    regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    
    match = re.search(regex, url)
    return match.group(1) if match else None  # Return video ID or None if not found

def get_youtube_video_url(id):
    '''
    Get youtube video url from short has
    '''

    return f"https://www.youtube.com/watch?v={id}"
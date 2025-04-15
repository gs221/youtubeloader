import yt_dlp
import random
from urllib.parse import urlparse, parse_qs

class YoutubeChannel: 
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.channel_url = f'https://www.youtube.com/@{channel_name}/videos'
        self.video_urls = dict()

    def scrape_video_urls(self):
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,  # Do not download, just get metadata
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.channel_url, download=False)
            entries = info.get('entries', [])

            for entry in entries:
                if self._accept_video(entry) and entry['url'] not in self.video_urls:
                    parsed_url = urlparse(entry['url'])
                    query_params = parse_qs(parsed_url.query)
                    video_id = query_params.get('v', [None])[0]
                    self.video_urls[video_id] = False # False means not watched yet

    def get_video_urls(self):
        return list(self.video_urls.keys())
    
    def get_unwatched_video_urls(self):
        unwatched = [url for url, watched in self.video_urls.items() if not watched]

        # If there are no unwatched videos, return all video URLs
        if len(unwatched) == 0:
            return self.get_video_urls()
        
        return unwatched
    
    def get_unwatched_video_url(self):
        unwatched = self.get_unwatched_video_urls()
        chosen_video = random.choice(unwatched)
        self.video_urls[chosen_video] = True
        return chosen_video
            
    def _accept_video(self, entry):
         return True
    

class YoutubeChannel48Hours(YoutubeChannel):
    def __init__(self):
        super().__init__('48hours')
    
    def _accept_video(self, entry):
        return "Full Episode" in entry['title'] and "Part" not in entry['title']
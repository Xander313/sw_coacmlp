from django import template
import re
from urllib.parse import quote

register = template.Library()

@register.filter
def embed_video(url):
    # YouTube
    youtube_match = re.search(r'(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|v/))([\w-]+)', url)
    if youtube_match:
        video_id = youtube_match.group(1)
        return f'''
        <div class="video-container">
            <iframe width="100%" height="100%"
                src="https://www.youtube.com/embed/{video_id}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
        </div>
        '''

    # Facebook - Versión optimizada
    if 'facebook.com' in url or 'fb.watch' in url:
        encoded_url = quote(url, safe='')
        return f'''
        <div class="video-container">
            <div class="video-wrapper">
                <iframe src="https://www.facebook.com/plugins/video.php?href={encoded_url}&show_text=false&width=560"
                    width="100%" height="100%"
                    scrolling="no"
                    frameborder="0"
                    allowfullscreen="true"
                    allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share">
                </iframe>
            </div>
        </div>
        '''

    
    return f'<a href="{url}" target="_blank">{url}</a>'
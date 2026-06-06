import json
import requests
from datetime import datetime

def create_playlist():
    json_url = "http://plex.uskamlesh3.serv00.net/adult-movies.json"
    base_url = "http://plex.uskamlesh3.serv00.net/" # এখানে বেস ইউআরএল সেট করা হয়েছে
    output_file = "playlist.m3u"
    
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    try:
        response = requests.get(json_url, headers=headers, timeout=15)
        data = response.json()
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            f.write(f"#EXTINF:-1,Playlist update: {now}\n")
            f.write("#EXTINF:-1,Playlist owner: STAR OTT BD\n")
            f.write("#EXTINF:-1,Playlist Creator: MD shakib Hasan\n")
            f.write("#EXTINF:-1,What's app: +8801610598422\n")
            f.write("#EXTINF:-1,Telegram: https://t.me/ibstvbd\n")
            f.write("#EXTINF:-1,Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")
            
            for item in data:
                name = item.get("name", "Unknown Stream")
                raw_url = item.get("direct_source", "")
                
                # [[SERVER_URL]] থাকলে সেটি মুছে ফেলে নতুন বেস ইউআরএল বসানো হচ্ছে
                clean_path = raw_url.replace("[[SERVER_URL]]/", "").replace("[[SERVER_URL]]", "")
                full_url = base_url + clean_path.lstrip('/') # পূর্ণাঙ্গ লিঙ্ক তৈরি
                
                f.write(f'#EXTINF:-1,{name}\n{full_url}\n')
                
        print(f"সফলভাবে প্লেলিস্ট আপডেট হয়েছে: {now}")
        
    except Exception as e:
        print(f"এরর: {e}")

if __name__ == "__main__":
    create_playlist()
    

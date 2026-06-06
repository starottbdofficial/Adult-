import json
import requests
from datetime import datetime

def create_playlist():
    # নতুন URL সেট করা হয়েছে
    json_url = "http://plex.uskamlesh3.serv00.net/adult-movies.json"
    output_file = "playlist.m3u"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(json_url, headers=headers, timeout=15)
        response.raise_for_status() 
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
                url = item.get("direct_source", "")
                
                # [[SERVER_URL]] থাকলে সেটি মুছে ফেলা হচ্ছে
                if url:
                    clean_url = url.replace("[[SERVER_URL]]/", "")
                    f.write(f'#EXTINF:-1,{name}\n{clean_url}\n')
                
        print(f"সফলভাবে প্লেলিস্ট আপডেট হয়েছে: {now}")
        
    except Exception as e:
        print(f"ডেটা ফেচ করতে সমস্যা হয়েছে: {e}")

if __name__ == "__main__":
    create_playlist()
    

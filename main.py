import json
import requests
from datetime import datetime

def create_playlist():
    json_url = "http://plex.uskamlesh3.serv00.net/adult-movies.json"
    output_file = "playlist.m3u"
    
    try:
        response = requests.get(json_url)
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
                name = item.get("name", "Unknown")
                url = item.get("direct_source", "")
                f.write(f'#EXTINF:-1,{name}\n{url}\n')
                
        print("Playlist generated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_playlist()
      

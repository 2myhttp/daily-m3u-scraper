import requests
from bs4 import BeautifulSoup
import os

# The URL to scrape
TARGET_URL = "https://iptvcat.net/venezuela__1"
OUTPUT_FILE = "venezuela.m3u"

def scrape_iptv():
    print(f"Fetching {TARGET_URL}...")
    
    # Fake a browser visit so the site doesn't block us
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(TARGET_URL, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching page: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Start the M3U content
    m3u_content = "#EXTM3U\n"
    count = 0

    # Logic: Find table rows, extract name and link
    # Note: Structure depends heavily on the specific website layout
    rows = soup.find_all("tr")
    
    for row in rows:
        # Try to find the link first
        link_tag = row.find("a", href=True)
        
        if link_tag:
            href = link_tag['href']
            
            # Check if it looks like a stream link
            if ".m3u8" in href or ".ts" in href or "http" in href:
                # Try to find a channel name in the row text
                name = row.get_text(strip=True).split('http')[0] # messy cleanup
                
                # If name is empty, use a default
                if len(name) < 2: 
                    name = "Unknown Channel"
                
                # Clean up the name
                name = name.replace(",", " ").strip()
                
                # Add to playlist
                m3u_content += f'#EXTINF:-1, {name}\n{href}\n'
                count += 1

    # Write to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"Finished! Found {count} channels.")

if __name__ == "__main__":
    scrape_iptv()

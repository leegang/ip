import requests
from bs4 import BeautifulSoup
import time

def scrape_cloudflare_ips():
    url = 'https://api.uouin.com/cloudflare.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    rows = soup.find_all('tr')
    
    ip_data = []
    for row in rows[1:]:  # Skip the header row
        columns = row.find_all('td')
        print(columns[0])
        if len(columns) >= 3:
            ip = columns[2].text.strip()
            network_type = columns[1].text.strip()
            ip_data.append(f"{ip}#{network_type}")
    
    filename = f'cloudflare_ips.txt'
    
    with open(filename, 'w', encoding='utf-8') as f:
        for line in ip_data:
            f.write(line + '\n')
    
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    scrape_cloudflare_ips()

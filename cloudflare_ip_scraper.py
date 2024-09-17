import requests
from bs4 import BeautifulSoup
import re

def fetch_and_parse(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def extract_ip_info(soup, url):
    ip_info = []
    
    if 'uouin.com' in url:
        rows = soup.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 3:
                ip = cols[1].text.strip()
                line = cols[0].text.strip()
                ip_info.append(f"{ip}#{line}")
    
    
    elif '090227.xyz' in url:
        rows = soup.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 3:
                ip = cols[1].text.strip()
                line = cols[0].text.strip()
                ip_info.append(f"{ip}#{line}")
    
    elif 'hostmonit.com' in url:
        ip_cells = soup.find_all('td', class_='el-table_3_column_16')
        colo_cells = soup.find_all('td', class_='el-table_3_column_22')
        for ip_cell, colo_cell in zip(ip_cells, colo_cells):
            ip = ip_cell.text.strip()
            colo = colo_cell.text.strip()
            ip_info.append(f"{ip}#{colo}")
    
    return ip_info

def main():
    urls = [
        "https://cf.090227.xyz/",
        "https://stock.hostmonit.com/CloudFlareYes",
        "https://api.uouin.com/cloudflare.html"
    ]
    
    all_ip_info = []
    
    for url in urls:
        try:
            soup = fetch_and_parse(url)
            ip_info = extract_ip_info(soup, url)
            all_ip_info.extend(ip_info)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
    
    # Remove duplicates and sort
    unique_ip_info = sorted(set(all_ip_info))

    
    
    # Save results to a txt file
    with open('cloudflare_ips.txt', 'w', encoding='utf-8') as f:
        for info in unique_ip_info:
            f.write(f"{info}\n")

if __name__ == "__main__":
    main()

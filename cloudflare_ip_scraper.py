import requests
from bs4 import BeautifulSoup
import re
import ipaddress
import json


import time

def fetch_and_parse(url):
    headers = {
        'Cache-Control': 'no-cache'
    }
    # 添加时间戳参数
    timestamp = int(time.time() * 1000)
    if  'hostmonit.com' in url:
        data = {"key": "iDetkOys"}
        response = requests.post(url + f"#ts={timestamp}", data = data)
    else:
        response = requests.get(url + f"#ts={timestamp}", headers=headers)
    
    return BeautifulSoup(response.text, 'html.parser')


def is_ipv6(ip):
    try:
        ipaddress.IPv6Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


def format_ip(ip, line):
    if is_ipv6(ip):
        return f"[{ip}]:80#{line}"
    else:
        return f"{ip}#{line}"

def extract_ip_info(soup, url):
    ip_info = []
    
    if 'uouin.com' in url:
        rows = soup.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 3:
                ip = cols[1].text.strip()
                line = cols[0].text.strip()
                ip_info.append(format_ip(ip, line))
    
    
    elif '090227.xyz' in url:
        rows = soup.find_all('tr')
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('td')
            if len(cols) >= 3:
                ip = cols[1].text.strip()
                line = cols[0].text.strip()
                ip_info.append(format_ip(ip, line))
    
    elif 'hostmonit.com' in url:
        text = json.loads(soup)
        ip_cell = text['ip']
        colo_cell = text['colo']
        for ip_cell, colo_cell in zip(ip_cells, colo_cells):
            try:
                ip = ip_cell.text.strip()
                colo = colo_cell.text.strip()
                ip_info.append(format_ip(ip, line))
            except Exception as e:
                print(f"Error processing cell: {e}")

    
    return ip_info

def main():
    urls = [
        # "https://cf.090227.xyz/",
        "https://api.uouin.com/cloudflare.html",
        "https://api.hostmonit.com/get_optimization_ip"
    ]
    
    all_ip_info = []
    
    for url in urls:
        print(f"processing {url}")
        try:
            print(f"try {url}")
            soup = fetch_and_parse(url)
            print(f":::soup:::\n {soup}")
            ip_info = extract_ip_info(soup, url)
            all_ip_info.extend(ip_info)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
    
    # Remove duplicates and sort
    unique_ip_info = sorted(set(all_ip_info))
    print(f"unique ip length:{len(unique_ip_info)}")
    
    
    # Save results to a txt file
    with open('cloudflare_ips.txt', 'w', encoding='utf-8') as f:
        for info in unique_ip_info:
            f.write(f"{info}\n")

if __name__ == "__main__":
    main()

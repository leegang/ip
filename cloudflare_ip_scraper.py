import requests
from bs4 import BeautifulSoup
import re
import ipaddress


def fetch_and_parse(url):
    headers = {
        'Cache-Control': 'no-cache'
    }
    response = requests.get(url, headers=headers)
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
        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        tuple_y = [(el, 7 * (el - 1) + 2, 7 * (el - 1) + 6) for el in x]
        cl = [(f"table_{y[0]}_column_{y[1]}", f"table_{y[0]}_column_{y[2]}") for y in tuple_y]
    
        ip_cells = []
        colo_cells = []
    
        for class_name in cl[0]:
            ip_cells.extend(soup.find_all('td', class_=class_name))
        for class_name in cl[1]:
            colo_cells.extend(soup.find_all('td', class_=class_name))
    
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
        "https://cf.090227.xyz/",
        "https://stock.hostmonit.com/CloudFlareYes",
        "https://api.uouin.com/cloudflare.html"
    ]
    
    all_ip_info = []
    
    for url in urls:
        print(f"processing {url}")
        try:
            print(f"try {url}")
            soup = fetch_and_parse(url)
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

import os
from colorama import init, Fore, Style
import argparse
import requests
init()

def scan_domain(domain):
    url = 'https://search.censys.io/api/v2/hosts/search'
    params = {
        'q': domain,
        'per_page': 50,
        'virtual_hosts': 'EXCLUDE',
        'sort': 'RELEVANCE'
    }
    headers = {
        'accept': 'application/json',
        'Authorization': 'Basic MDMwMGVkODQtYTY4ZS00MmU1LWIyZjYtYzQ2YWM3MDYzNDJlOlJLdWJaVVo0N0wyOTRCTFhCNWJmVjhQTndDOUNHUTBx'
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        ip_addresses = data['result']['hits']

        if not ip_addresses:
            print(Fore.RED + "[!]No IP addresses found.")
            return

        output_folder = "output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_file = os.path.join(output_folder, f"{domain}-scan.txt")
        with open(output_file, "w") as file:
            file.write("===Scan Result===\n\n")
            file.write(f"[+] {len(ip_addresses)} results found\n\n")
            for ip_data in ip_addresses:
                ip = ip_data['ip']
                services = ip_data['services']
                file.write("[--------------------------]\n")
                file.write(f"-> IP address: {ip}\n")
                for service in services:
                    details = f"{service['extended_service_name']} (Port: {service['port']})"
                    file.write(f"{details}\n")
                file.write("[--------------------------]\n\n")
                print("[--------------------------]")
                print(f"-> IP address: {ip}")
                for service in services:
                    details = f"{service['extended_service_name']} (Port: {service['port']})"
                    print(details)
                print("[--------------------------]")

        print(Fore.LIGHTGREEN_EX + f"[+]Results file saved to: {output_file}")

    else:
        print(Fore.RED + f'[!]Error searching for {domain}')

if __name__ == "__main__":
    print(r"""  _   _      _   _____           _     
 | \ | |    | | |  __ \         | |    
 |  \| | ___| |_| |__) | __ ___ | |__  
 | . ` |/ _ \ __|  ___/ '__/ _ \| '_ \ 
 | |\  |  __/ |_| |   | | | (_) | |_) |
 |_| \_|\___|\__|_|   |_|  \___/|_.__/ 
                                       
                                       

""")
    print("["+Fore.BLUE+ "INF"+Style.RESET_ALL+"]This tool was coded by LAPSUS and is public.")
    print("["+Fore.BLUE+ "INF"+Style.RESET_ALL+"]Telegram : t.me/LAPSUS\n")
    parser = argparse.ArgumentParser(description='Domain Scanner')
    parser.add_argument('-u', '--url', type=str, help='URL of the website to scan')
    args = parser.parse_args()
    
    if args.url:
        scan_domain(args.url)
    else:
        print(Fore.YELLOW + "[-]Please specify the URL of the website to scan using the -u or --url argument.")

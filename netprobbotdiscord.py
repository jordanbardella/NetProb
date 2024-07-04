import discord
from discord.ext import commands, tasks
import aiohttp
import json
import aiofiles
import asyncio
import subprocess
import re
import aiohttp 
from colorama import init, Fore, Style
import base64
import requests 
import os
from tls_client import Session
from terminut import printf as print, inputf as input
from os import system; system('cls||clear')

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} connected!')

async def scan_domain(domain):
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
            return None

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

        print(Fore.LIGHTGREEN_EX + f"[+]Results file saved to: {output_file}")
        return output_file

    else:
        print(Fore.RED + f'[!]Error searching for {domain}')
        return None

@bot.command(name='scan')
async def scan_domain_command(ctx, domain: str):
    output_file = await scan_domain(domain)
    if output_file:
        await ctx.send(file=discord.File(output_file))


    
bot.run('')

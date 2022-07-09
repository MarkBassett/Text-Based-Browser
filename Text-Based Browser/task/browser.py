import sys
import os
import re
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore


directory = sys.argv[1]
cwd = os.getcwd()
folder = os.path.join(cwd, directory)
if not os.path.isdir(directory):
    os.makedirs(folder)

stack = deque()

def file_print(file):
    soup = BeautifulSoup(file.content, 'html.parser')
    for i in soup.findAll('a'):
        if i.text:
            i.string = i.text.replace(i.text, Fore.BLUE + i.text + Fore.RESET)
    page = soup.text
    page = page.split('\n')
    page = [p for p in page if len(p) > 0]
    page = '\n'.join(page)
    print(page)
    return page


file_name = ''
string = None
while True:
    search = input()
    is_url = bool(re.search(r'\w+\.\w+', search))
    if search == 'exit':
        break
    elif is_url:
        if string:
            stack.append(string)
        starts_http = bool(re.search('^https://', search))
        if not starts_http:
            search = 'http://' + search
        response = requests.get(
            search,
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;qf=0.8',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0'},
        )
        if response.status_code == 200:
            string = file_print(response)
            search = search.strip('https://')
            file_name = search.split('.')[-2]
            file = os.path.join(folder, file_name)
            with open(file, 'w') as f:
                f.write(string)
        else:
            print('Error: Incorrect URL')
    elif search == file_name:
        if string:
            stack.append(string)
        with open(file, 'r') as f:
            string = f.read()
        print(string)
    elif search == 'back':
        if len(stack) > 0:
            string = stack.pop()
    else:
        print('Error: Incorrect URL')

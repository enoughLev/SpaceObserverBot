import requests
from bs4 import BeautifulSoup
import re
from config import URL_MKS


def get_iss_status():
    r = requests.get(URL_MKS)
    soup = BeautifulSoup(r.text, 'html.parser')

    for span in soup.find_all("span", class_="info-text"):
        i = span.find("i", class_="min-info")
        if i and "дня на орбите" in i.text:
            days_text = span.find(text=True, recursive=False)
            days = int(days_text.strip())
            return days if days else 'N/A'


def get_iss_crew():
    url = "https://mks-online.ru/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    crew_data = []
    crew_blocks = soup.find_all('div', class_='crew-item')

    for block in crew_blocks:
        team_name_tag = block.find('p', class_='vertical-info')
        if not team_name_tag:
            continue
        team_name = team_name_tag.get_text(strip=True)

        members = block.find_all('div', class_='item')
        for member in members:
            img_div = member.find('div', class_='post-img-middle')
            if not img_div or 'style' not in img_div.attrs:
                img_url = None
            else:
                img_style = img_div['style']
                match = re.search(r"url\('(.+?)'\)", img_style)
                img_url = match.group(1) if match else None

            name_tag = member.find('div', class_='post-title-middle')
            if not name_tag or not name_tag.p:
                name = "Без имени"
            else:
                name = name_tag.p.get_text(strip=True)

            crew_data.append({
                'team': team_name,
                'name': name,
                'photo': img_url
            })

    return crew_data

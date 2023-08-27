import requests
import re
from bs4 import BeautifulSoup

def get_internships():
    url = "https://raw.githubusercontent.com/pittcsc/Summer2024-Internships/dev/README.md"
    site_content = requests.get(url)

    text = site_content.content

    all_internships = text[text.find(b'| ---- | -------- | ----- |')+30:text.find(b'\n\n<!-- Please leave ')]
    internship_list = re.split(rb'(\|\n\||\n\|)', all_internships)

    internship_list = [item for item in internship_list if item != b'|\n|' and item != b'\n|']

    return internship_list

def new_internships(internships, intern_num = 1):
    new_intern_list = internships[intern_num*-1:]
    new_intern_list = [item.decode('UTF-8').split('|') for item in new_intern_list]
    
    return new_intern_list

def get_internship_title(internship):
    title_info = internship[0]
    company_pattern = r"\[(.*?)\]"
    website_pattern = r"\((https?://.*?)\)"
    company_match = re.search(company_pattern, title_info)
    website_match = re.search(website_pattern,title_info)
    if company_match:
        title = company_match.group(1)
        link = website_match.group(1).strip()
    else:
        title = title_info
        link = None
    return title.strip(), link

def get_locations(internship):
    locations = internship[1].split('<br/>')
    embed = '**Locations:\n** '
    embed += "\n".join(locations).strip()

    return embed

def intern_dictionary(internship):
    internship_dict = {}
    internships = internship[2].split('<br/>')
    role_pattern = r"\[(.*?)\]"
    website_pattern = r"\((https?://.*?)\)"

    for i in internships:
        role_match = re.search(role_pattern, i)
        website_match = re.search(website_pattern,i)
        if role_match:
            role = role_match.group(1).strip()
            website = website_match.group(1).strip()
        else:
            role = i.strip()
            website = 0
        internship_dict[role] = website

    return internship_dict


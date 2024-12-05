import re
import urllib.request

import requests


def download_file(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url, cookies=cookies)
        # write to file
        file.write(response.content)
        print(f"Downloaded: {file_name}")


# Set the corse url you want to download the file from
course_url = "https://didatticaonline.unitn.it/dol/course/view.php?id=courseid"

# Set your cookies to have access to the course (just copy them from one request
cookies_string = "yourcookie1=something; yourcookie2=somethingelse;"

cookies = {}

for s in cookies_string.split(";"):
    splitted = s.split("=")
    cookies[splitted[0].strip()] = splitted[1].strip()

first_layer_urls = []
second_layer_urls = []

res = requests.get(course_url, cookies=cookies)

first_pattern = "https?:\/\/didatticaonline.unitn.it\/dol\/mod\/resource\/view.php?[^\"\'&]*"
first_re = re.compile(first_pattern)

res1 = re.findall(first_pattern, res.text)

for link in res1:
    if link not in first_layer_urls:
        first_layer_urls.append(link)

second_pattern = "https?:\/\/didatticaonline.unitn.it\/dol\/pluginfile.php\/\d+\/mod_resource[^\"\'&]*"

for current_url in first_layer_urls:
    res = requests.get(current_url, cookies=cookies)
    res2 = re.findall(second_pattern, res.text)

    for link in res2:
        if link not in second_layer_urls:
            second_layer_urls.append(link)
            print(f"Found file: {link}")

for file_url in second_layer_urls:
    download_file(file_url, file_url.split("/")[-1])

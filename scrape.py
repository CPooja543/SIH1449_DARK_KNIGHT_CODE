import re
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def fetch_first_cve_result(keyword):
    # print(keyword)
    url = f'https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query={keyword}&queryType=phrase&search_type=all&isCpeNameSearch=false'
    response = requests.get(url)
    list1 = []
    print(f'**Scanning for {keyword}**')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', class_='table')
   
    if table:
        rows = table.find_all('tr')
        if len(rows)<2:
            print(f'NO vulnerable components detected for {keyword}')
            return 
        front = []
        other = []
        for row in rows:
            th_element = row.find('th', {'nowrap': 'nowrap'})
            td_element = row.find_all('td')
        
            if th_element:
                front.append(th_element.text.strip())
            for i in td_element:
                    other.append(i.text.strip())
        result = front[1]
        print(result)
        list1.append(result)
        temp = str(other[0])

        date_pattern = re.compile(r'\b\d{1,2}/\d{1,2}/\d{4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\b')

        matches = date_pattern.findall(temp)

        date_result = []
        for match in matches:
            date_result = match
        list1.append(date_result)
        print(date_result)
        vuln_rows = soup.find_all('tr', {'data-testid': 'vuln-row-'})
        for row in vuln_rows:
            span_element = row.find('span', {'id': 'cvss3-link'})
            if span_element:
                anchor_element = span_element.find('a')
            if anchor_element:
                anchor_content = anchor_element.text.strip()
                print( anchor_content)
        if table:
            rows = table.find('tbody').find_all('tr')
            for row in rows:
                span_element = row.find('span', id='cvss3-link')
            if span_element:
                cvss_severity = span_element.text.strip()
                list1.append(cvss_severity)
                print("CVSS Severity:", cvss_severity)
                # return list1
        
# def run():
#     url = 'http://localhost:8080/dependencies'
#     response = requests.get(url)
#     final = {}
#     if response.status_code == 200:
#         final = response.json()
#         for item in final['result']:
#             print(fetch_first_cve_result(item['name']),end='\n')
final = {
  "result": [
    {
      "name": "prop-types",
      "platform": "npm",
      "version": "^15.6.2"
    },
    {
      "name": "react",
      "platform": "npm",
      "version": "^16.6.3"
    },
    {
      "name": "react-dom",
      "platform": "npm",
      "version": "^16.6.3"
    },
    {
      "name": "react-scripts",
      "platform": "npm",
      "version": "2.1.1"
    },
    {
        "name":"log4j",
        "platform":"java",
        "version":"20.2.1", 
    }
  ]
}
# data2 = [{"name": "absl-py",
#                     "platform": "unknown",
#                     "version": "1.4.0"

#             },
#             {
#                     "name": "accelerate",
#                     "platform": "unknown",
#                     "version": "0.22.0"
#             },
#             {
#                 "name": "aiofiles",
#                 "platform": "unknown",
#                 "version": "23.2.1"
#             },]
#             # {
#             #     'name' : 'log4j',
#             #     'platform' : 'unknown',
#             #     'version' : '20.0.1'
#             # }]
for item in final['result']:
    temp = []
    temp =  fetch_first_cve_result(item["name"])
    # print(item["name"])  
# print(list1,end='\n')
# print(list2,end='\n')
# print(list3,end='\n')
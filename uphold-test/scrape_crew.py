from requests import get
from bs4 import BeautifulSoup
import json
import pandas as pd

top50 = pd.read_csv('../top50/top50.csv', header=0)
rate_limited = False

for index, row in top50.iterrows():
    if rate_limited:
        break
    url = row['url'] + 'fullcredits'
    response = get(url)

    crew_names = []
    onset_crew = ['Directed by', 'Cinematography by', 'Production Management',
                  'Second Unit Director or Assistant Director',
                  'Sound Department', 'Camera and Electrical Department']

    soup = BeautifulSoup(response.text, 'html.parser')

    for h4, table in zip(soup.find_all('h4'), soup.find_all('table')):
        header4 = " ".join(h4.text.strip().split())
        if header4 not in onset_crew:
            continue
        table_data = [" ".join(tr.text.strip().replace("\n", "").replace("...", "|").split())  for tr in table.find_all('tr')]
        for listing in table_data:
            name = listing.split('|')[0]
            first_name = name.split(' ')[0]
            crew_names.append(first_name)

    crew_names = [name for name in crew_names if len(name) > 0]

    genders = {}
    for index in range(len(crew_names) + 1):
        if rate_limited:
            break
        subset = crew_names[index:index+1]
        api = 'https://api.genderize.io/?'
        for i, name in enumerate(subset):
            api += 'name[' + str(i) + ']=' + name.lower()
        req = get(api)
        results = json.loads(req.text)
        for result in results:
            try:
                if result['gender'] is None:
                    genders[result['name']] = [None]
                    continue
            except:
                print("We got rate limited. :(")
                rate_limited = True
                break

            genders[result['name']] = [result['gender'], result['probability'],
                                       result['count']]

    with open(row['title'] + '.json', 'w') as fp:
        json.dump(genders, fp)

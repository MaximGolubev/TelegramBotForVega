import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста


with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# print (data_text['settings']['firstWeekDate'])

def search_by_group(group):
    group = group.upper()
    for gr in data['groups']:
        if gr['group'] == group:
            return json.dumps(gr['days'], indent=4)
    return 'Error!'
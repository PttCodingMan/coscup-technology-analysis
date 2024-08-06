import os

import requests


def main():
    sources = {
        '2024': 'https://pretalx.coscup.org/api/events/coscup-2024/talks/?format=json&limit=1000',
        '2023': 'https://pretalx.coscup.org/api/events/coscup-2023/talks/?format=json&limit=1000',
        '2022': 'https://pretalx.com/api/events/coscup-2022/talks/?format=json&limit=1000',
        '2021': 'https://coscup.org/2021/json/session.json',
        '2020': 'https://coscup.org/2020/json/session.json'
    }

    for year, url in sources.items():

        if os.path.exists(f'./raw_data/coscup-{year}.txt'):
            pass
        else:
            r = requests.get(url)

            if year in ['2021', '2020']:
                sessions = r.json()['sessions']

                content = ''
                for s in sessions:
                    current_data = ''
                    if 'zh' in s:
                        current_data += s['zh']['title'] + '\n'
                        current_data += s['zh']['description'] + '\n'
                    elif 'en' in s:
                        current_data += s['en']['title'] + '\n'
                        current_data += s['en']['description'] + '\n'

                    current_data = current_data.replace('\r\n', '\n')
                    while '\n\n' in current_data:
                        current_data = current_data.replace('\n\n', '\n')

                    current_data = current_data.strip()

                    if current_data == '':
                        continue

                    content += f'{current_data}\n=======\n'

            else:
                data = r.json()['results']

                content = ''
                for d in data:

                    current_data = ''
                    if d['description'] == d['abstract']:
                        if d['description'] and len(d['description']) > 0:
                            current_data += d['description'] + '\n'
                    else:
                        current_data += d['abstract'] + '\n'
                        current_data += d['description'] + '\n'

                    current_data = current_data.replace('\r\n', '\n')
                    while '\n\n' in current_data:
                        current_data = current_data.replace('\n\n', '\n')

                    current_data = current_data.strip()

                    if current_data == '':
                        continue

                    content += f'{current_data}\n=======\n'

            with open(f'./raw_data/coscup-{year}.txt', 'w') as f:
                f.write(content)

        print(f'coscup-{year}.txt done')


if __name__ == '__main__':
    main()

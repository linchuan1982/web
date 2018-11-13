from datetime import datetime, timedelta
import re
import requests
from bs4 import BeautifulSoup


def _get_offset_or_views(meta):
    if 'view' in meta:
        meta_type = 'views'
        views = int(''.join(re.findall('\d', meta.split()[0])))
        return meta_type, views
    elif 'ago' in meta:
        meta_type = 'publish_at'
        delta = meta.split()
        if 'week'in delta[-2]:
            offset = timedelta(weeks=int(delta[-3]))
        elif 'day' in delta[-2]:
            offset = timedelta(days=int(delta[-3]))
        elif 'hour' in delta[-2]:
            offset = timedelta(hours=int(delta[-3]))
        elif 'month' in delta[-2]:
            offset = timedelta(days=int(delta[-3]) * 30)
        elif 'year' in delta[-2]:
            offset = timedelta(days=int(delta[-3]) * 365)
        else:
            offset = None
        if offset:
            publish_at = datetime.now() - offset
        else:
            print('no offset {}'.format(meta))
            publish_at = None
        return meta_type, publish_at
    else:
        print('no type {}'.format(meta))
        return None, None


def extract_one_page(soup, summ):

    divs = soup.find_all('div', class_='yt-lockup-content')
    if not divs:
        return

    for div in divs:
        info = dict()
        link = div.select('h3 a')[0]
        info['url'] = link['href']
        info['title'] = link['title']
        div_meta_info = div.find('ul', class_='yt-lockup-meta-info')
        if div_meta_info:
            li_metas = div_meta_info.find_all('li')
            # meta 有点乱，可能只有views，也可能只包含发布时间
            for meta in li_metas:
                _type, value = _get_offset_or_views(meta.get_text())
                if _type:
                    info[_type] = value
        else:
            # print('no meta info in div {}'.format(div))
            continue
        summ.append(info)

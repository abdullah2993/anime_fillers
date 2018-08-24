import urllib2
import json
from bs4 import BeautifulSoup


def get_shows():
    results = []
    source = get_source('shows')
    if source is None:
        return results

    soup = BeautifulSoup(source, 'html.parser')
    main_list = soup.find('div', {'id': 'ShowList'})
    if main_list is None:
        print "unable to find list"
        return results

    for li in main_list.find_all('li'):
        results.append({'name': unicode(li.a.string.strip()), 'id': li.a['href'].replace('/shows/', '')})
    return results


def get_show(id):
    results = []
    source = get_source('shows/' + id)
    if source is None:
        return results

    soup = BeautifulSoup(source, 'html.parser')
    main_table = soup.find('table', {'class': 'EpisodeList'})
    if main_table is None:
        print "unable to find table"
        return results
    if main_table.tbody is None:
        print "unable to find table body"
        return results

    for row in main_table.tbody.find_all("tr"):
        cols = row.find_all('td')
        if len(cols) != 4:
            print "invalid row found"
            continue
        no = int(cols[0].string.strip())
        title = unicode(cols[1].a.string.strip())
        status = cols[2].span.string.strip()
        date = '' if (cols[3].string is None) else cols[3].string.strip()
        results.append({'no': no, 'title': title, 'type': status, 'date': date})
    return results


def get_source(link):
    source = None
    try:
        source = urllib2.urlopen('https://www.animefillerlist.com/' + link).read()
    except urllib2.URLError as err:
        print "unable to load page: ", err
    return source


def main():
    shows = get_shows()
    with open('shows.json', 'w') as sf:
        json.dump(shows, sf)

    for i, show in enumerate(shows):
        print "getting", show['name'].encode('utf8'), i + 1, 'of', len(shows)
        eps = get_show(show['id'])
        with open(show['id'] + '.json', 'w') as ef:
            json.dump(eps, ef)


if __name__ == '__main__':
    main()

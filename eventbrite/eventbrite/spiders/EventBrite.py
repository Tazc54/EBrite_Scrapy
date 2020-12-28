import scrapy
import json


class EventbriteSpider(scrapy.Spider):
    name = 'EventBrite'
    start_urls = ['https://www.eventbrite.com/api/v3/destination/search/', ]
    headers = {
        'Referer': 'https://www.eventbrite.com/d/united-states/business--classes/?page=1',
        'X-CSRFToken': '2974cf82480811eba4a84b61040b14e4',
        'Content-Type': 'application/json',
    }
    cookies = {'csrftoken': '2974cf82480811eba4a84b61040b14e4; Path=/; Domain=.eventbrite.com; Secure; '
                            'Expires=Sun, 26 Dec 2021 05:55:46 GMT;'}

    def start_requests(self):
        # currently just testing 3 categoryes, with 3 formats each and 3 pages from each format
        for i in range(101, 103): #121
            for j in range(1, 3): #20
                for k in range(1, 3):#20
                    payload = "{\"event_search\":{\"dates\":\"current_future\",\"dedup\":false,\"places\":[\"85633793\"]," \
                              "\"tags\":[\"EventbriteCategory/"+str(i)+"\",\"EventbriteFormat/"+str(j)+"\"],\"page\":"+str(k)+",\"page_size\":50," \
                              "\"online_events_only\":false,\"client_timezone\":\"America/Mexico_City\"}," \
                              "\"expand.destination_event\":[\"primary_venue\",\"image\",\"ticket_availability\"," \
                              "\"saves\",\"my_collections\",\"event_sales_status\"]} "
                    yield scrapy.Request(url='https://www.eventbrite.com/api/v3/destination/search/',
                                         headers=self.headers,
                                         cookies=self.cookies,
                                         body=payload,
                                         method='POST', callback=self.parse)

    def parse(self, response, **kwargs):
        online_event = False
        jsonresponse = json.loads(response.text)
        print(response)
        results = jsonresponse['events']['results']
        images = []
        event_name = []
        event_start_date = []
        event_start_time = []
        event_end_date = []
        event_end_time = []
        event_category = []
        event_format = []
        event_organizer = []
        event_location = []
        event_url = []
        event_location_type = []
        for result in results:
            if 'image' in result.keys():
                images.append(result['image']['url'])
            else:
                images.append('https://www.allianceplast.com/wp-content/uploads/2017/11/no-image.png')

            event_name.append(result['name'])
            event_start_date.append(result['start_date'])
            event_start_time.append(result['start_time'])

            if result['hide_end_date'] == 'false':
                event_end_date.append(result['end_date'])
            else:
                event_end_date.append('N/A')
            if result['end_time'] is not None:
                event_end_time.append(result['end_time'])
            else:
                event_end_time.append('N/A')
            event_category.append(result['tags'][0]['display_name'])
            event_format.append(result['tags'][1]['display_name'])
            event_organizer.append({'organizer_name': result['id'], 'organizer_description': 'N/A',
                                    'organizer_profile_url': f'https://www.eventbrite.com/ajax/event/{result["id"]}'
                                                             f'/related/same-organizer/?aff=erelpanel',
                                    'organizer_total_events': 'N/A'})
            if result['is_online_event'] == 'false' or 'ONLINE' not in result['primary_venue']['name'].upper():
                event_location.append({'street_address_1': result['primary_venue']['address']})
            else:
                online_event = True
                event_location.append('Online Event')
            event_url.append(result['url'])
            if online_event:
                event_location_type.append('Online')
            else:
                event_location_type.append('OnPrem')
        yield {
            'event_name': event_name,
            'event_start_date': event_start_date,
            'event_start_time': event_start_time,
            'event_end_date': event_end_date,
            'event_end_time': event_end_time,
            'event_category': event_category,
            'event_format': event_format,
            'event_organizer': event_organizer,
            'event_location': event_location,
            'event_url': event_url,
            'event_location_type': event_location_type,
            'image_urls': images,
        }

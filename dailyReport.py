import requests
from bs4 import BeautifulSoup


# TODO:Consider adding ascii art for weather? If cloudy, sunny, rainy?
#websites for reference for when making readme:https://www.weather.gov/documentation/services-web-ap; https://open-meteo.com/en/docs
# https://pollenandmold.stlouisco.com/
#obtain information about the office which is required for the NWS API, it uses the coordinates of your current location
#display to the terminal the current forecast, the current local alerts if any, and the current state alerts if any

page = requests.get('https://pollenandmold.stlouisco.com/')

soup = BeautifulSoup(page.content, 'html.parser')

page_title = soup.title
page_body = soup.body

text = soup.select('tbody')[2]

local_zone = "MOZ063"
county_zone = "MOC189"
state_area = "MO"
coords = {"latitude": 38.5951,"longitude": -90.5462}

elements_list = []
def get_text_from_site(text):
    for element in text:
        formatted_element = element.get_text(strip=True)
        if formatted_element:
            elements_list.append(formatted_element)
    # print(elements_list[:-1])
    new_string = "\n".join(elements_list[1:-1])
    print(new_string)


def get_office_information(latitude, longitude):
    response = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
    response.raise_for_status()

    return response

office_information = get_office_information(**coords).json()
forecast = requests.get(office_information['properties']['forecast']).json()

# request the information for the local alerts using the zone requested (local is a much narrower search, county expands the request)
def get_local_alerts(zone):
    response = requests.get(f"https://api.weather.gov/alerts/active?zone={zone}")
    response.raise_for_status()

    return response

# request the information for the alerts using the state_area requested
def get_state_alerts(area):
    response = requests.get(f"https://api.weather.gov/alerts/active?area={area}")
    response.raise_for_status()

    return response

#request the daily forecast using the office information and returning the 'detailedForecast' 
def display_forecast(forecast):
    detailed_forecast =  forecast['properties']['periods'][0]['detailedForecast']
    
    return detailed_forecast

def display_local_alerts(zone):
    alerts = get_local_alerts(zone).json()
    #this will work if we are not sure if 'features' exists, it will return an empty array
    if not alerts.get('features', []):
        return "No current active local alerts to display."
    else:
        for alert in alerts['features']:
            alert_headline = alert['properties']['headline']
            alert_description = alert['properties']['description']
            alert_instructions = alert['properties']['instruction']
       

        return [alert_headline, alert_description, alert_instructions]
    
def display_state_alerts(area):
    alerts = get_state_alerts(area).json()
    if not alerts.get('features', []):
        return "No current active alerts to display."
    else:
        # need to account for if more than one alert is available
        for alert in alerts['features']:
            alert_headline = alert['properties']['headline']
            alert_description = alert['properties']['description']
            alert_instructions = alert['properties']['instruction']
    
    return [alert_headline, alert_description, alert_instructions]



print('*' * 50)
print("Current Forecast:")
print(display_forecast(forecast))
print('*' * 50)
print("Current Local Alerts:")
final_local_alerts = display_local_alerts(local_zone)
for line in final_local_alerts:
    print(line)
# print(final_local_alerts)
print('*' * 50)
print("Current State Alerts:")
final_state_alerts = display_state_alerts(state_area)
for alert in final_state_alerts:
    print(alert)
print('*' * 50)
print("Most Recent Pollen and Mold Report:")
get_text_from_site(text)
print('*' * 50)
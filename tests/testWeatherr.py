import requests
import json


def __getWheather(city,link):
    headers = {'Content-Type': 'application/json'}


    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def get_weather(city):
    api_url_base = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + "&units=metric&lang=nl&APPID=8434e7589baa7da22d0220b2669daef0"
    return __getWheather(city,api_url_base)


def get_weatherForCast(city):
    api_url_base = 'https://api.openweathermap.org/data/2.5/orecast/daily?q='+city+"&APPID=8434e7589baa7da22d0220b2669daef0"
    return __getWheather(city, api_url_base)



def main():
    print("start")
    res=get_weather("dendermonde")

    if res is not None:
        print("Here's your info: ")
        for k, v in res.items():
            print('{0}:{1}'.format(k, v))

    else:
        print('[!] Request Failed')
    a = input("return to stop")


if __name__ == "__main__":
    main()

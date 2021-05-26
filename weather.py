import requests

import geo_localization
from internet_connection import isConnectedToInternet
from datetime import datetime
import errors as err
from author_data import email

# defined weather options
current_temperature = 1
today_weather = 2
today_is_raining = 3
tomorrow_weather = 4
day_after_tomorrow_weather = 5
next_hours_weather = 6

# If you want to use weather api you must generate your api key from https://openweathermap.org/ and assign it to variable api_key
api_key = "4a84c7a8412f04b9b7d5acd62b40df4f"

msg_error_connection = "I am sorry, but I have to work on my connection with current weather data. " \
                       "If you want to report the problem, contact my author by email: {}".format(email)

msg_no_internet = "If you want to check the weather you must be connected with the Internet."

msg_hope_sunny = "I really hope that it is a sunny day. " \
                         "If you want to report the problem, contact my author by email: {}".format(email)


# does not consider hours
def areDatesTheSame(date1, date2):
    if date1.day == date2.day and date1.month == date2.month and date1.year == date2.year:
        return True
    return False


def get_lat_long(cityName, isPrintingErrors=False):
    url = "https://api.openweathermap.org/data/2.5/find?q=" + cityName
    url += "&units=metric&appid=" + api_key
    try:
        response = requests.get(url)
        response.raise_for_status()  # raise exception if status is other than 200
        response_json = response.json()
        if response_json['count'] == 0:
            return err.error_city_name, "I'm sorry but I don't know city named {}".format(cityName)
        else:
            coord = response_json['list'][0]['coord']
            lat = coord['lat']
            lon = coord['lon']
            return 0, (str(lat), str(lon))
    except requests.exceptions.HTTPError as http_ex:
        if isPrintingErrors:
            print(f'HTTP error occurred: {http_ex}')
    except Exception as ex:
        if isPrintingErrors:
            print(f'Error occurred: {ex}')

    return err.error_api_connection, msg_error_connection


def get_icon(number):
    response = requests.get("https://openweathermap.org/img/wn/" + number + "@2x.png")
    fileName = "weather_icons/" + number + ".png"
    file = open(fileName, "wb")
    file.write(response.content)
    file.close()
    return fileName


def current_weather_url(cityName=None):
    if isConnectedToInternet(isPrintingErrors=False):
        if cityName is None:
            error, result = geo_localization.lat_long_gps()
        else:
            error, result = get_lat_long(cityName)
        if error != 0:
            return error, result
        else:
            (lat, lon) = result
            url = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon
            url += "&units=metric&appid=" + api_key
            return 0, url
    else:
        return err.error_no_internet, msg_no_internet


def detail_weather_url(cityName=None):
    if isConnectedToInternet(False):
        if cityName is None:
            error, result = geo_localization.lat_long_gps()
        else:
            error, result = get_lat_long(cityName)
        if error != 0:
            return error, result
        else:
            (lat, lon) = result
            url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lon
            url += "&exclude={daily}&units=metric&appid=" + api_key
            return 0, url
    else:
        return err.error_no_internet, msg_no_internet


# returns 1 if there was some errors - 0 otherwise
def current_weather_response(cityName=None, isPrintingErrors=False):
    try:
        error, result = current_weather_url(cityName)
        if error != 0:
            error_description = result
            return error, error_description
        else:
            url = result
            response = requests.get(url)
            response.raise_for_status()
            response_json = response.json()
            city_name = response_json["name"]
            curr_temp = response_json["main"]["temp"]
            feels_temp = response_json['main']['feels_like']
            description = response_json['weather'][0]['description']
            weather_icon = response_json['weather'][0]['icon']

            msg_temp = "The temperature now in {} is {} Celcius degrees and it feels like {}. ".format(city_name, round(curr_temp), round(feels_temp))
            msg_descr = "There is a " + description +"."
            return 0, (msg_temp, msg_descr, get_icon(weather_icon))

    except requests.exceptions.HTTPError as http_ex:
        error = err.error_api_connection
        error_description = "I am sorry, but I have to work on my connection with weather data. "
        if isPrintingErrors:
            print(f'HTTP error occurred: {http_ex}')
    except Exception as ex:
        error = err.error_api_response
        error_description = "I am sorry, but I have some problems with sharing the weather forecast with you. "
        if isPrintingErrors:
            print(f'Error occurred: {ex}')

    error_description += msg_hope_sunny
    return error, error_description


def detail_weather_response(isHourly, cityName=None, isPrintingErrors=False):
    hourly_map = {}
    daily_map = {}
    try:
        error, result = detail_weather_url(cityName)
        if error != 0:
            error_description = result
            return error, error_description
        else:
            url = result
            response = requests.get(url)
            response.raise_for_status()
            response_json = response.json()
            if isHourly:  #hourly_data
                iter = 0
                for elem in response_json['hourly']:
                    date = datetime.utcfromtimestamp(elem['dt'])
                    iter += 1
                    if iter > 9:
                        break
                    if areDatesTheSame(date, datetime.today()):
                        temp = elem['temp']
                        feels_temp = elem['feels_like']
                        clouds = elem['clouds']
                        wind_speed = elem['wind_speed']
                        main = elem['weather'][0]['main']
                        description = elem['weather'][0]['description']
                        icon = elem['weather'][0]['icon']
                        hourly_weather = temp, feels_temp, main, description, clouds, wind_speed, get_icon(icon)
                        hourly_map[date] = hourly_weather

                return 0, hourly_map
            else:    #daily_data
                for elem in response_json['daily']:
                    date = datetime.utcfromtimestamp(elem['dt'])
                    temp = elem['temp']['day']
                    feels_temp = elem['feels_like']['day']
                    daily_min = elem['temp']['min']
                    daily_max = elem['temp']['max']
                    wind_speed = elem['wind_speed']
                    clouds = elem['clouds']
                    main = elem['weather'][0]['main']
                    description = elem['weather'][0]['description']
                    icon = elem['weather'][0]['icon']

                    daily_weather = temp, feels_temp, daily_min, daily_max, main, description, clouds, wind_speed, get_icon(icon)
                    daily_map[date] = daily_weather

                return 0, daily_map

    except requests.exceptions.HTTPError as http_ex:
        error = err.error_api_connection
        error_description = "I am sorry, but I have to work on my connection with weather data. "
        if isPrintingErrors:
            print(f'HTTP error occurred: {http_ex}')
    except Exception as ex:
        error = err.error_api_response
        error_description = "I am sorry, but I have some problems with sharing the weather forecast with you. "
        if isPrintingErrors:
            print(f'Error occurred: {ex}')

    error_description += msg_hope_sunny
    return error, error_description


def getFutureDailyForecast(whichOneInTheFuture, cityName=None, isPrintingErrors = False):
    error, result = detail_weather_response(False, cityName, isPrintingErrors)  #False -> daily response
    if error != 0:
        return error, result
    else:
        daily_map = result
        values = daily_map.values()
        value_iterator = iter(values)
        for i in range(whichOneInTheFuture):
            data = next(value_iterator)
        return 0, (daily_weather_description(data[0], data[1], data[2], data[3], data[5]), data[8])


def daily_weather_description(temp, feels_temp, daily_min, daily_max, description):
    return "The temperature will be {} Celcius degrees and it will feels like {}. Maximum daily temperature will be {}, and " \
           "minimum will be {}. There will be {}.".format(round(temp), round(feels_temp), round(daily_max), round(daily_min), description)


def getFutureHourlyForecast(cityName=None, isPrintingErrors = False):
    error, result = detail_weather_response(True, cityName, isPrintingErrors)
    if error != 0:
        return error, result
    else:
        hourly_map = result
        hourly_descr = []
        hourly_icons = []
        iter = 0
        for date in hourly_map:
            if areDatesTheSame(date, datetime.today()):
                iter += 1
                if iter > 5:
                    break
                if iter > 2:
                    forecast_data = hourly_map[date]
                    hour = date.strftime('%H:%M')
                    hourly_descr.append(hourly_weather_description(hour, forecast_data[0], forecast_data[1], forecast_data[3]))
                    hourly_icons.append(forecast_data[6])
        return 0, (hourly_descr, hourly_icons)


def hourly_weather_description(hour, temp, feels_temp, description):
    return "The temperature at {} will be {} Celcius degrees and it will feel like {}. There will be {}.\n".format(hour, round(temp), round(feels_temp), description)


def isRainingToday(cityName=None, isPrintingErrors=False):
    errCode, result = detail_weather_response(True, cityName, isPrintingErrors)
    if errCode != 0:
        return errCode, result
    else:
        hourly_map = result
        for date in hourly_map:
            if areDatesTheSame(date, datetime.today()):
                if hourly_map[date][2] == "Rain":
                    return 0, "Today will be raining. If you go out, you might take an umbrella with you."
        return 0, "Today won't be raining."


def make_weather_response(option, cityName=None, isPrintingErrors=False):
    if option == current_temperature:
        error, result = current_weather_response(cityName, isPrintingErrors)
        temp_description = result
        if error == 0:
            temp_description = (result[0], result[2])
        return error, temp_description    # for error=0, temp_desc [1] is an icon's filename
    elif option == today_weather:
        return current_weather_response(cityName, isPrintingErrors)    # for error=0, tuple[1] is an icon's filename
    elif option == today_is_raining:
        return isRainingToday(cityName, isPrintingErrors)
    elif option == tomorrow_weather:
        return getFutureDailyForecast(1, cityName, isPrintingErrors)
    elif option == day_after_tomorrow_weather:
        return getFutureDailyForecast(2, cityName, isPrintingErrors)
    elif option == next_hours_weather:
        return getFutureHourlyForecast(cityName, isPrintingErrors)


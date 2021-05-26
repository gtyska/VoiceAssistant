import speech_recog as my_sr
import web_search as ws
import time
import re
import weather
import wikipedia
import requests
import errors as err
from author_data import email

msg_other_error = "I am sorry, but I have some problems with sharing this information with you at the moment. " \
                  "If you want to report the problem, contact my author by email: " + email


def introduction():
    my_sr.intro()


def error_and_message():
    return my_sr.get_message()


def weather_for_city(option_, city_name, isPrintingErrors=False):
    attempt_counter = 0
    while True:
        attempt_counter += 1
        if attempt_counter > 3:
            return err.error_city_name, "I am sorry, but I don't know the names of the cities that you told me."
        error, result = weather.make_weather_response(option=option_, cityName=city_name,
                                                      isPrintingErrors=isPrintingErrors)
        if error != err.error_city_name:
            return error, result
        else:
            my_sr.speak("The city named {} does not exist. Pleas say the name of the city once again.".format(
                city_name))
            error, city_name = my_sr.get_message()
            if error != 0:
                return err.error_recognition, "I am sorry but I couldn't recognize your voice."


def open_yt(query=None):
    try:
        ws.open_yt(query)
        return 0, "YouTube is opened in your browser"
    except Exception:
        return err.error_no_internet, "YouTube can't be opened. Please check your Internet connection."


def open_google(query=None):
    try:
        ws.open_google(query)
        return 0, "Google is opened in your browser"
    except Exception:
        return err.error_no_internet, "Google can't be opened. Please check your Internet connection"


def run(error_and_message, isPrintingErrors=False):
    error = error_and_message[0]
    message = error_and_message[1]
    if error != 0:
        return error, message
    message = message.lower()

    if "my name is" in message:
        name = message.split(' ')[-1]
        my_sr.saveName(name)
        msg_new_name = "From now on I will call you {}".format(name)
        return 0, msg_new_name

    elif ("search " in message or "open " in message) and " on google" in message:
        left = ""
        if "search " in message:
            left = "search "
        elif "open " in message:
            left = "open "

        try:
            query = re.search(re.escape(left) + "(.*)" + re.escape(" on google"), message).group(1)
        except Exception:
            msg_not_supported = "I am sorry, but I don't support that question."
            return 0, msg_not_supported
        return open_google(query)

    elif "open google " in message:
        return open_google()

    elif "what time is it" in message or "what hour is it" in message:
        str_time_now = time.strftime("%I:%M %p.", time.localtime())
        msg_time = "It is " + str_time_now
        return 0, msg_time

    elif "how are you" in message:
        msg = "I am well, thank you."
        return 0, msg

    elif "open you tube" in message or "open youtube" in message:
        return open_yt()

    elif "on youtube" in message or "on you tube" in message:
        left = ""
        if "play me" in message:
            left = "play me "
        elif "play" in message:
            left = "play "
        elif "open me" in message:
            left = "open me "
        elif "open" in message:
            left = "open"

        if "on youtube" in message:
            right = "on youtube"
        else:
            right = "on you tube"

        try:
            query = re.search(re.escape(left) + "(.*)" + re.escape(right), message).group(1)
        except Exception:
            msg_not_supported = "I am sorry, but I don't support that question."
            return 0, msg_not_supported

        return open_yt(query)

    elif "temperature" in message and "is" in message:
        splitted_message = message.split(" ")
        len_message = len(splitted_message)
        city_name = None
        if splitted_message[len_message - 2] == "in":
            city_name = splitted_message[len_message - 1]

        err_code, result = weather.make_weather_response(1, cityName=city_name, isPrintingErrors=isPrintingErrors)
        if err_code != 0:
            return err_code, result
        else:
            msg = result[0]
            icon = result[1]
            return 0, (msg, icon)

    elif ("raining" in message or "rain" in message or "umbrella" in message) and ("today" in message):
        city_name = None
        if " in " in message:
            try:
                city_name = re.search(re.escape("in ") + "(.*)", message).group(1)
                city_name = city_name.split(" ")[0]
            except Exception:
                msg_not_supported = "I am sorry, but I don't support that question."
                return 0, msg_not_supported

        error, result = weather_for_city(option_=3, city_name=city_name, isPrintingErrors=isPrintingErrors)

        return error, result

    elif "weather" in message:
        city_name = None
        isTodaysWeather = False
        if "tomorrow" in message:
            city_name = None
            if " in " in message:
                try:
                    city_name = re.search(re.escape("in ") + "(.*)", message).group(1)
                    city_name = city_name.split(" ")[0]
                except Exception:
                    msg_not_supported = "I am sorry, but I don't support that question."
                    return 0, msg_not_supported

            error, result = weather_for_city(option_=4, city_name=city_name, isPrintingErrors=isPrintingErrors)

            if error != 0:
                return error, result
            else:
                weather_descr = result[0]
                icon = result[1]
                return 0, (weather_descr, icon)

        elif "day after tomorrow" in message:
            if " in " in message:
                try:
                    city_name = re.search(re.escape("in ") + "(.*)", message).group(1)
                    city_name = city_name.split(" ")[0]
                except Exception:
                    msg_not_supported = "I am sorry, but I don't support that question."
                    return 0, msg_not_supported

            error, result = weather_for_city(option_=5, city_name=city_name, isPrintingErrors=isPrintingErrors)

            if error != 0:
                return error, result
            else:
                weather_descr = result[0]
                icon = result[1]
                return 0, (weather_descr, icon)

        elif "hours" in message or "hourly" in message or "nearest time" in message:
            if " in " in message:
                try:
                    city_name = re.search(re.escape("in ") + "(.*)", message).group(1)
                    city_name = city_name.split(" ")[0]
                except Exception:
                    msg_not_supported = "I am sorry, but I don't support that question."
                    return 0, msg_not_supported

            error, result = weather_for_city(option_=6, city_name=city_name, isPrintingErrors=isPrintingErrors)

            if error != 0:
                return error, result
            else:
                hourly_descr = result[0]
                hourly_icons = result[1]
                msg_hourly = ""
                for hour_forecast in hourly_descr:
                    msg_hourly += hour_forecast + " "
                return 0, (msg_hourly, hourly_icons[0])

        elif (" is " in message or "what's" in message or "today" in message) and "in" in message:
            try:
                city_name = re.search(re.escape("in ") + "(.*)", message).group(1)
            except Exception:
                msg_not_supported = "I am sorry, but I don't support that question."
                return 0, msg_not_supported
            city_name = city_name.split(" ")[0]
            isTodaysWeather = True

        if " is " in message or "what's" in message:
            isTodaysWeather = True
        if isTodaysWeather:
            option_ = 2
            if "tomorrow" in message:
                option_ = 4

            error, result = weather_for_city(option_=option_, city_name=city_name, isPrintingErrors=isPrintingErrors)

            if error != 0:
                return error, result
            else:
                len_res = len(result)
                if len_res == 3:
                    weather_descr = result[0] + " " + result[1]
                    icon = result[2]
                    return 0, (weather_descr, icon)
                else:  # len_res = 2
                    weather_descr = result[0]
                    icon = result[1]
                    return 0, (weather_descr, icon)
        else:
            err_code, result = weather.make_weather_response(option=2, isPrintingErrors=isPrintingErrors)
            if err_code != 0:
                return err_code, result
            else:
                msg = result[0]
                icon = result[1]
                return 0, (msg, icon)

    elif "what is " in message or "who is " in message:
        if "what is " in message:
            try:
                definition = re.search(re.escape("what is ") + "(.*)" + re.escape(""), message).group(1)
            except Exception:
                msg_not_supported = "I am sorry, but I don't support that question."
                return 0, msg_not_supported
        else:
            try:
                definition = re.search(re.escape("who is ") + "(.*)" + re.escape(""), message).group(1)
            except Exception:
                msg_not_supported = "I am sorry, but I don't support that question."
                return 0, msg_not_supported
        try:
            result = wikipedia.summary(definition, sentences=2)
            return 0, result
        except wikipedia.PageError:
            return err.error_wiki_definition_not_found, "I am sorry but {} was not found on the wikipedia".format(
                definition)
        except requests.exceptions.ConnectionError:
            return err.error_no_internet, "If you want to have an access to wikipedia, you must have an Internet connection."
        except Exception:
            return err.error_other, msg_other_error

    else:
        msg_not_supported = "I am sorry, but I don't support that question."
        return 0, msg_not_supported


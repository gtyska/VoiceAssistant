import webbrowser

URL_google = 'http://google.com'
URL_yt = 'https://www.youtube.com/results?search_query='


def open_yt(query=None):
    if query is None:
        webbrowser.open("https://www.youtube.com", new=2)
    else:
        converted_query = query.replace(' ', '+')
        url = URL_yt+converted_query
        webbrowser.open(url, new=2)


def open_google(query=None):
    if query is None:
        webbrowser.open(URL_google, new=2)
    else:
        url = URL_google + "?q=" + query
        webbrowser.open(url, new=2)


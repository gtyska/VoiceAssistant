import urllib.request


def isConnectedToInternet(isPrintingErrors=False):
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except Exception:
        if isPrintingErrors:
            print("Error - no internet connection")
        return False

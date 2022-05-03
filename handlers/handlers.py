import re
def check_url(url: str) -> bool:
    result = re.findall(r'^[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#-=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', url)
    if result:
        return True
    else:
        return False






CACHE = {}

def get(url):
    return CACHE.get(url)

def set(url, file_id):
    CACHE[url] = file_id

import json
import random

from helpers_for_json.utils4json import send_request


IPINFO_URL: str = "https://ipinfo.io/{}/json"


async def url(ipv4: str, useragents: list[str]) -> dict:
    """
    Get the details of the IP address from the IPInfo API.

    Args:
        ipv4: str
            The IP address to get the details of.
        useragents: list[str]
            The list of user agents.

    Returns:
        retdict: dict
            The details of the IP address.
    """
    url = str(IPINFO_URL).format(ipv4)
    response = await send_request(url, headers={"User-Agent": random.choice(useragents)})

    return json.loads(response.text)


async def look_ipinfo(ipv4: str, useragents: list[str]) -> dict:
    """
    Get the details of the IP address from the IPInfo API.
    
    Args:
        ipv4: str
            The IP address to get the details of.
        useragents: list[str]
            The list of user agents.
    
    Returns:
        retdict: dict
            The details of the IP address.
    """
    track = await url(ipv4, useragents)
    coordinates = {track['loc']}
    lat = str(coordinates).split(",")[0].replace("{", "").replace("'", "")
    long = str(coordinates).split(",")[1].replace("}", "").replace("'", "")

    try:
        hostname = track['hostname']
    except:
        hostname = None
    try:
        org = track['org']
    except:
        org = None

    retdict = {
        "hostname": hostname,
        "org": org,
        "country": track['country'],
        "region": track['region'],
        "city": track['city'],
        "latitude": lat,
        "longitude": long
    }
    
    return retdict





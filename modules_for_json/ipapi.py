import json
import random

from helpers_for_json.utils4json import send_request


IP_API_URL: str = "http://ip-api.com/json/{}"


async def url(ipv4: str, useragents: list[str]) -> dict:
    """
    Get the details of the IP address from the IP API.

    Args:
        ipv4: str
            The IP address to get the details of.
        useragents: list[str]
            The list of user agents.

    Returns:
        retdict: dict
            The details of the IP address.
    """
    url = str(IP_API_URL).format(ipv4)
    response = await send_request(url, headers={"User-Agent": random.choice(useragents)})

    return json.loads(response.text)


async def lookup(ipv4: str, useragents: list[str]) -> dict:
    """
    Get the details of the IP address from the IP API.
    
    Args:
        ipv4: str
            The IP address to get the details of.
        useragents: list[str]
            The list of user agents.
    
    Returns:
        retdict: dict
            The details of the IP address.
    """
    read = await url(ipv4, useragents)
    
    org: str = read['org']
    country: str = read['country']
    region: str = read['regionName']
    city: str = read['city']

    retdict = {
        "org": org,
        "country": country,
        "region": region,
        "city": city,
    }

    return retdict


import json
import random

from helpers_for_json.utils4json import send_request


IP_WHOIS_URL: str = "http://ipwho.is/{}"


async def url(ipv4: str, useragents: list[str]) -> dict:
    """
    Get the details of the IP address from the IP Whois API.

    Args:
        ipv4: str
            The IP address to get the details of.
        useragents: list[str]
            The list of user agents.

    Returns:
        retdict: dict
            The details of the IP address.
    """
    url = str(IP_WHOIS_URL).format(ipv4)
    response = await send_request(url, headers={"User-Agent": random.choice(useragents)})

    return json.loads(response.text)


async def look_whois(ipv4: str, useragents: list[str]) -> dict:
    """
    Get the details of the IP address from the IP Whois API.
    
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
    
    continent = read['continent']
    country = read['country']
    region = read['region']
    city = read['city']
    isp = read['connection']['isp']
    domain = read['connection']['domain']
    org = str(domain).split(".")[0]
    
    retdict = {
        "continent": continent,
        "country": country,
        "region": region,
        "city": city,
        "isp": isp,
        "domain": domain,
        "organization": org
    }

    return retdict

import asyncio
import json
import random

from ScrapeSearchEngine.SearchEngine import Google

from helpers_for_json.utils4json import send_request


PASTEBIN_URL: str = "https://pastebin.com/"
PASTEBIN_RAW_URL: str = "https://pastebin.com/raw/"


async def pastebin_check(search_result_link: str, ipv4: str, useragents: list[str]) -> str | None:
    """
    Check if the IP address is present in the Pastebin link.

    Args:
        search_result_link: str
            The search result link.
        ipv4: str
            The IP address to check.
        useragents: list[str]
            The list of user agents.

    Returns:
        link: str
            The Pastebin link if the IP address is present in the link.
    """
    try:
        link = str(search_result_link).replace(PASTEBIN_URL, PASTEBIN_RAW_URL)
        data = await send_request(link, headers={"User-Agent": random.choice(useragents)})

        if ipv4.lower() in data.text.lower() or ipv4 in data.text or ipv4.upper() in data.text.upper():
            return link
    
    except Exception as e:
        return None


async def pastebin_dump(ipv4: str, useragents: list[str]) -> list[str]:
    """
    Get the Pastebin links that contain the IP address.

    Args:
        ipv4: str
            The IP address to check.
        useragents: list[str]
            The list of user agents.

    Returns:
        links: list[str]
            The list of Pastebin links that contain the IP address.
    """
    search_query = ("site:pastebin.com \"{}\"".format(ipv4))
    try:
        google_text, google_links = Google(
            search=search_query,
            userAgent=random.choice(useragents),
        )
        
        result_links = []
        for link in google_links:
            result = await pastebin_check(link, ipv4, useragents)
            if result is not None:
                result_links.append(result)
        
        await asyncio.gather(*result_links)
        
        return result_links

    except Exception as e:
        return []


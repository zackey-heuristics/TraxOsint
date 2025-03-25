import re
import httpx


URL_TO_GET_USERAGENTS: str = "https://raw.githubusercontent.com/zackey-heuristics/SpyScraper/refs/heads/master/useragents.txt"


async def send_request(url: str, headers: dict[str, str], timeout: int = 10) -> httpx.Response:
    """
    Send a request to the URL.
    
    Args:
        url: str
            The URL to send the request to.
        headers: dict[str, str]
            The headers to be sent with the request.
        timeout: int
            The timeout for the request.
    
    Returns:
        response: httpx.Response
            The response of the request.
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response
    except httpx.HTTPStatusError as e:
        raise e
    except httpx.RequestError as e:
        raise e
    except Exception as e:
        raise e


async def get_useragents_from_github(url_to_get_useragents: str = "") -> list[str]:
    """
    Get the list of user agents from the GitHub repository.
    
    Returns:
        useragents: list[str]
            The list of user agents.
    """
    if url_to_get_useragents == "":
        url: str = URL_TO_GET_USERAGENTS
    else:
        url: str = url_to_get_useragents
    
    try:
        response = await send_request(url, headers={})
        useragents = response.text.splitlines()
        return useragents
    except httpx.HTTPStatusError as e:
        raise e
    except httpx.RequestError as e:
        raise e
    except Exception as e:
        raise e
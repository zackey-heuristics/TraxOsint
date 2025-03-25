import os


async def ping(ipv4: str) -> int:
    """
    Ping the IP address.  

    Args:
        ipv4: str
            The IP address to be pinged.
    
    Returns:
        response: int
            The response code of the ping.
    """
    response = os.system(
        f'ping -n 1 {ipv4} > nul' if os.name == "nt" else f'ping -c 1 {ipv4} > /dev/null 2>&1'
    )

    return response
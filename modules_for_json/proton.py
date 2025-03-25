import random
import re

from helpers_for_json.utils4json import send_request


PROTON_VPN_CHECK_URL: str = "https://api.protonmail.ch/vpn/logicals"


async def vpnchecker(ipv4: str, useragents: list[str]) -> dict:
    """
    Check if the IP address is affiliated with ProtonVPN.

    Args:
        ipv4: str
            The IP address to be checked.
        useragents: list[str]
            The list of user agents.

    Returns:
        retdict: dict
            The output of the check.
    """
    response = await send_request(PROTON_VPN_CHECK_URL, headers={"User-Agent": random.choice(useragents)})

    try:
        if ipv4 in response.text:
            retdict = {
                "status": "success", 
                "result": "affiliated",
                "message": "This IP address is currently affiliated with ProtonVPN."
            }

        else:
            retdict = {
                "status": "success",
                "result": "not_affiliated",
                "message": "This IP address is not currently affiliated with ProtonVPN."
            }
    except Exception:
        retdict = {
            "status": "error",
            "result": "rate_limit",
            "message": "ProtonRate limit."
        }

    return retdict

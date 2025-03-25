"""
This module is used to output the TraxOsint result in JSON format.

Usage:
    python traxosint_json_output.py [IPV4] [--useragent USERAGENT] [--only-passive-check] [--output OUTPUT_JSON_FILE_PATH]

Options:
    IPV4: str
        The IP address to be queried.
    USER_AGENT: str
        The user-agent to be used in the request header.
        When “random” is set, a user-agent is selected at random from the list of user-agents prepared in advance.
        Default is “random”.
    OUTPUT_JSON_FILE_PATH: pathlib.Path
        The output JSON file path.
    ---
    --only-passive-check: bool
        Perform only passive checks.
        Default is True.
"""
import argparse
from ast import arg
import asyncio
import datetime
from http.client import TOO_EARLY
import json
import pathlib
import re
import sys


from lib_for_json.pinger4json import ping
from lib_for_json.check_ports4json import check_open_ports
from modules_for_json.proton import vpnchecker
from modules_for_json.pastebin import pastebin_dump
from modules_for_json.ipinfo import look_ipinfo
from modules_for_json.ipwhois import look_whois
from modules_for_json.ipapi import lookup
from helpers_for_json.utils4json import get_useragents_from_github, send_request


# The regular expression pattern for the IPv4 address.
IP_V4_REGEX_PATTERN: str = r'^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'
# The list of target ports to be checked.
TARGET_PORTS: list[int] = [8080, 80, 443]


async def maincore():
    parser = argparse.ArgumentParser(
        description="Output the TraxOsint result in JSON format."
    )
    parser.add_argument(
        "ipv4",
        type=str,
        help="The IP address to be queried."
    )
    parser.add_argument(
        "--useragent",
        type=str,
        default="random",
        help="The user-agent to be used in the request header. When “random” is set, a user-agent is selected at random from the list of user-agents prepared in advance.",
    )
    parser.add_argument(
        "--only-passive-check",
        action="store_true",
        default=True,
        help="Perform only passive checks."
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="The output JSON file path."
    )
    args = parser.parse_args()
    target_ipv4: str = args.ipv4
    output_json_file_path = args.output
    is_only_passive_check: bool = args.only_passive_check
    
    if not re.match(IP_V4_REGEX_PATTERN, target_ipv4):
        print("Invalid IP address.", file=sys.stderr)
        sys.exit(1)
    
    if args.useragent == "random":
        try:
            useragents = await get_useragents_from_github()
        except Exception as e:
            print(f"Failed to get user agents: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        useragents = [args.useragent]
    
    if not is_only_passive_check:
        ping_response: int = await ping(target_ipv4)
        if ping_response == 0:
            ping_response_dict = {"status": "success", "message": "The target is reachable."}
        else:
            ping_response_dict = {"status": "error", "message": "The target is not reachable."}
        open_ports_dict: dict = await check_open_ports(target_ipv4, TARGET_PORTS)
    else:
        ping_response_dict = {}
        open_ports_dict = {}
        
    protonvpn_response_dict: dict = await vpnchecker(target_ipv4, useragents)
    pastebin_responses: list = await pastebin_dump(target_ipv4, useragents)
    ip_info_response_dict: dict = await look_ipinfo(target_ipv4, useragents)
    whois_response_dict: dict = await look_whois(target_ipv4, useragents)
    ipapi_response_dict: dict = await lookup(target_ipv4, useragents)
    
    results = {
        "ping": ping_response_dict,
        "open_ports": open_ports_dict,
        "protonvpn": protonvpn_response_dict,
        "pastebin": pastebin_responses,
        "ipinfo": ip_info_response_dict,
        "whois": whois_response_dict,
        "ipapi": ipapi_response_dict
    }
    
    if output_json_file_path:
        with open(output_json_file_path, "w") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"{output_json_file_path.resolve()}")
    else:
        print(json.dumps(results, indent=4, ensure_ascii=False))
    
    
def main():
    asyncio.run(maincore())
    
    
if __name__ == "__main__":
    main()

import socket


async def check_open_ports(ipv4: str, ports: list[int]) -> dict:
    """
    Check the open ports of the IP address.
    
    Args:
        ipv4: str
            The IP address to be checked.
        ports: list[int]
            The list of ports to be checked.
    
    Returns:
        open_ports: dict
            The dictionary containing the open ports.
    """
    open_ports: dict = {}
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ipv4, port))
            sock.close()
            
            if result == 0:
                open_ports[port] = "open"
            else:
                open_ports[port] = "closed"
        except Exception as e:
            open_ports[port] = f"error: {e}"
    
    return open_ports
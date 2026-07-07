import socket


def get_mac_address(interface):
    """
    Returns the MAC address of the given interface as bytes.
    """

    try:
        with open(f"/sys/class/net/{interface}/address", "r") as f:
            mac = f.read().strip()
    except OSError as e:
        raise RuntimeError(f"Unable to read MAC address of {interface}") from e

    return bytes.fromhex(mac.replace(":", ""))


def format_mac(mac):
    """
    Converts MAC bytes into a printable string.
    Example:
        b'\x00\x0c)...' -> 00:0C:29:71:E7:74
    """
    return ":".join(f"{b:02X}" for b in mac)

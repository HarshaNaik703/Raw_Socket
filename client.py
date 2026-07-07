
import socket
import struct

from protocol import *
from interface import *

# =====================================================
# CHANGE THESE
# =====================================================

INTERFACE = "ens33"

# Server MAC Address
DESTINATION_MAC = bytes.fromhex(
    "000C293EFF0B"
)

# =====================================================

sock = socket.socket(
    socket.AF_PACKET,
    socket.SOCK_RAW,
    socket.htons(CUSTOM_ETHERTYPE)
)

sock.bind((INTERFACE, 0))

source_mac = get_mac_address(INTERFACE)

# Build Ethernet Header
ethernet_header = struct.pack(
    "!6s6sH",
    DESTINATION_MAC,
    source_mac,
    CUSTOM_ETHERTYPE
)

# Build Payload
payload = create_connection_packet("Hello Server")

# Complete Ethernet Frame
frame = ethernet_header + payload

# Send
sock.send(frame)

print("Connection Request Sent.")

# Wait for ACK
while True:

    response = sock.recv(1500)

    dest_mac, src_mac, ethertype = struct.unpack(
        "!6s6sH",
        response[:14]
    )

    if ethertype != CUSTOM_ETHERTYPE:
        continue

    payload = response[14:14 + PACKET_SIZE]

    version, packet_type, length, message = unpack_packet(payload)

    if packet_type != CONNECTION_ACK:
        continue

    print("\n===== ACK Received =====")
    print("Version     :", version)
    print("Packet Type :", packet_type)
    print("Length      :", length)
    print("Message     :", message)
    print("Source MAC  :", format_mac(src_mac))
    print("Dest MAC    :", format_mac(dest_mac))
    print("========================")

    break

sock.close()

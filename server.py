import socket
import struct

from protocol import *
from interface import *

# =====================================================
# CHANGE THIS IF YOUR INTERFACE IS DIFFERENT
# =====================================================

INTERFACE = "ens33"

# =====================================================

sock = socket.socket(
    socket.AF_PACKET,
    socket.SOCK_RAW,
    socket.htons(CUSTOM_ETHERTYPE)
)

sock.bind((INTERFACE, 0))

print(f"Listening on {INTERFACE}")
print("=" * 50)
print("Waiting for Connection Request...")
print("=" * 50)

server_mac = get_mac_address(INTERFACE)

while True:

    frame = sock.recv(1500)

    # Ethernet header is always 14 bytes
    dest_mac, src_mac, ethertype = struct.unpack(
        "!6s6sH",
        frame[:14]
    )

    if ethertype != CUSTOM_ETHERTYPE:
        continue

    payload = frame[14:14 + PACKET_SIZE]

    version, packet_type, length, message = unpack_packet(payload)

    if packet_type != CONNECTION_REQUEST:
        continue

    print("\n===== Connection Request Received =====")
    print(f"Version      : {version}")
    print(f"Packet Type  : {packet_type}")
    print(f"Length       : {length}")
    print(f"Message      : {message}")
    print(f"Source MAC   : {format_mac(src_mac)}")
    print(f"Destination  : {format_mac(dest_mac)}")
    print("=======================================\n")

    # Create ACK payload
    ack_payload = create_ack_packet("Connection Accepted")

    # Ethernet header
    ack_header = struct.pack(
        "!6s6sH",
        src_mac,
        server_mac,
        CUSTOM_ETHERTYPE
    )

    ack_frame = ack_header + ack_payload

    sock.send(ack_frame)

    print("ACK sent successfully.")

    

sock.close()

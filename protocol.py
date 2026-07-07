import struct

# =====================================================
# Custom EtherType
# =====================================================
CUSTOM_ETHERTYPE = 0x88B5

# =====================================================
# Protocol Version
# =====================================================
PROTOCOL_VERSION = 1

# =====================================================
# Packet Types
# =====================================================
CONNECTION_REQUEST = 1
CONNECTION_ACK = 2

# =====================================================
# Packet Layout
#
# uint8_t  version
# uint8_t  packet_type
# uint16_t message_length
# char     message[64]
# =====================================================

MAX_MESSAGE_LEN = 64

PACKET_FORMAT = "!BBH64s"
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)


def create_packet(message, packet_type):
    """
    Creates a protocol packet.
    """

    if isinstance(message, str):
        message = message.encode("utf-8")

    # Save actual message length
    message_length = min(len(message), MAX_MESSAGE_LEN)

    # Truncate if necessary
    message = message[:MAX_MESSAGE_LEN]

    # Pad to exactly 64 bytes
    message = message.ljust(MAX_MESSAGE_LEN, b"\x00")

    return struct.pack(
        PACKET_FORMAT,
        PROTOCOL_VERSION,
        packet_type,
        message_length,
        message
    )


def create_connection_packet(message):
    return create_packet(message, CONNECTION_REQUEST)


def create_ack_packet(message="Connection Accepted"):
    return create_packet(message, CONNECTION_ACK)


def unpack_packet(packet_bytes):
    """
    Converts bytes back into Python values.
    """

    version, packet_type, length, message = struct.unpack(
        PACKET_FORMAT,
        packet_bytes
    )

    message = message[:length].decode("utf-8")

    return version, packet_type, length, message

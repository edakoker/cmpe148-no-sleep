# src/protocol/messages.py

DELIMITER = "|"


def build_message(msg_type: str, payload: str, client_id: str = "", seq: int = 0) -> bytes:
    """
    Build an application-layer message in the format:
    VERSION|TYPE|CLIENT_ID|SEQ|LENGTH\nPAYLOAD

    and return it as bytes ready to be sent over the socket.
    """
    version = "1"

    # Encode the payload and compute its length in bytes
    payload_bytes = payload.encode("utf-8")
    length = len(payload_bytes)

    # Build the header line
    header = f"{version}{DELIMITER}{msg_type}{DELIMITER}{client_id}{DELIMITER}{seq}{DELIMITER}{length}\n"

    # Concatenate header and payload as bytes
    full_message = header.encode("utf-8") + payload_bytes
    return full_message


def parse_message(raw_bytes: bytes) -> dict:
    """
    Parse a raw message (bytes) and return a dictionary with fields:
    version, type, client_id, seq, length, payload.

    Expected format:
    VERSION|TYPE|CLIENT_ID|SEQ|LENGTH\\nPAYLOAD
    """
    text = raw_bytes.decode("utf-8")

    # Split into header and payload using the first newline
    try:
        header_line, payload = text.split("\n", 1)
    except ValueError:
        raise ValueError("Invalid message: missing header or payload")

    parts = header_line.split(DELIMITER)
    if len(parts) != 5:
        raise ValueError("Invalid header: wrong number of fields")

    version, msg_type, client_id, seq_str, length_str = parts

    # Convert numeric fields
    try:
        seq = int(seq_str)
        length = int(length_str)
    except ValueError:
        raise ValueError("Invalid header: SEQ or LENGTH is not an integer")

    # Optional: verify that LENGTH matches the actual payload length
    payload_bytes = payload.encode("utf-8")
    if len(payload_bytes) != length:
        # For now, we just ignore the mismatch.
        # Later we could raise an error or log a warning here.
        pass

    return {
        "version": version,
        "type": msg_type,
        "client_id": client_id,
        "seq": seq,
        "length": length,
        "payload": payload,
    }
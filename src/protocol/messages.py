# src/protocol/messages.py

DELIMITER = "|"


def build_message(msg_type: str, payload: str, client_id: str = "", seq: int = 0) -> bytes:
    """
    Uygulama seviyesindeki bir mesaji
    VERSION|TYPE|CLIENT_ID|SEQ|LENGTH\nPAYLOAD
    formatina cevirir ve bytes olarak dondurur.
    """
    version = "1"

    # payload'i utf-8'e cevirip uzunlugunu hesapla
    payload_bytes = payload.encode("utf-8")
    length = len(payload_bytes)

    # header satirini olustur
    header = f"{version}{DELIMITER}{msg_type}{DELIMITER}{client_id}{DELIMITER}{seq}{DELIMITER}{length}\n"

    # header + payload'i birlestirip bytes'a cevir
    full_message = header.encode("utf-8") + payload_bytes
    return full_message


def parse_message(raw_bytes: bytes) -> dict:
    """
    Raw bytes olarak gelen mesaji cozup
    bir dict olarak dondurur.
    Beklenen format:
    VERSION|TYPE|CLIENT_ID|SEQ|LENGTH\\nPAYLOAD
    """
    text = raw_bytes.decode("utf-8")

    # header ve payload'i ayir (ilk \\n'a gore)
    try:
        header_line, payload = text.split("\n", 1)
    except ValueError:
        raise ValueError("Invalid message: missing header or payload")

    parts = header_line.split(DELIMITER)
    if len(parts) != 5:
        raise ValueError("Invalid header: wrong number of fields")

    version, msg_type, client_id, seq_str, length_str = parts

    # sayisal alanlari cevir
    try:
        seq = int(seq_str)
        length = int(length_str)
    except ValueError:
        raise ValueError("Invalid header: SEQ or LENGTH is not an integer")

    # istege bagli: length ile payload uzunlugu uyusuyor mu kontrol edelim
    payload_bytes = payload.encode("utf-8")
    if len(payload_bytes) != length:
        # Simdilik sadece warning gibi dusunelim, hata da verebilirdik
        # ama projenin ilerleyen kisminda burada sikica kontrol yapabiliriz.
        pass

    return {
        "version": version,
        "type": msg_type,
        "client_id": client_id,
        "seq": seq,
        "length": length,
        "payload": payload,
    }
"""Utility functions related to genshin fuckery"""
import hashlib
import random
import re
import string
import time
from typing import Optional, Union

__all__ = [
    "generate_ds_token",
    "create_short_lang_code",
    "recognize_server",
    "recognize_id",
    "is_genshin_uid",
    "is_chinese",
]


def generate_ds_token(salt: str) -> str:
    """Creates a new ds token for authentication."""
    t = int(time.time())
    r = "".join(random.choices(string.ascii_letters, k=6))
    h = hashlib.md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest()
    return f"{t},{r},{h}"


def create_short_lang_code(lang: str) -> str:
    """Returns an alternative short lang code"""
    return lang if "zh" in lang else lang.split("-")[0]


def recognize_server(uid: int) -> str:
    """Recognizes which server a UID is from."""
    server = {
        "1": "cn_gf01",
        "5": "cn_qd01",
        "6": "os_usa",
        "7": "os_euro",
        "8": "os_asia",
        "9": "os_cht",
    }.get(str(uid)[0])

    if server:
        return server
    else:
        raise ValueError(f"UID {uid} isn't associated with any server")


def recognize_id(id: int) -> Optional[str]:
    """Attempts to recognize what item type an id is"""
    # TODO: Return the model (might be a problem with characters)
    if 10000000 < id < 20000000:
        return "Character"
    elif 1000000 < id < 10000000:
        return "ArtifactSet"
    elif 100000 < id < 1000000:
        return "Outfit"
    elif 50000 < id < 100000:
        return "Artifact"
    elif 10000 < id < 50000:
        return "Weapon"
    elif 100 < id < 1000:
        return "Constellation"
    elif 10 ** 17 < id < 10 ** 19:
        return "Transaction"
    else:
        return None


def is_genshin_uid(uid: int) -> bool:
    """Recognizes whether the uid is a valid genshin uid."""
    return bool(re.fullmatch(r"[6789]\d{8}", str(uid)))


def is_chinese(x: Union[int, str]) -> bool:
    """Recognizes whether the server/uid is chinese."""
    return str(x).startswith(("cn", "1", "5"))

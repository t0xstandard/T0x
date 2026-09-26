#!/usr/bin/env python3
"""T-Zero timestamp standard reference implementation.

Format: YYYYMMDDTHHMMSS.sss (19 chars, UTC, fixed-width)
"""

import re
from datetime import datetime, timezone

FMT = re.compile(
    r"^(?P<y>\d{4})(?P<m>\d{2})(?P<d>\d{2})"
    r"T(?P<H>\d{2})(?P<M>\d{2})(?P<S>\d{2})"
    r"(?:\.(?P<ms>\d{1,3}))?$"
)


def validate(s):
    """Return (True, 'ok') if s is a valid T-Zero timestamp, else (False, reason)."""
    m = FMT.match(s)
    if not m:
        return False, "format mismatch"
    y, mo, d, H, Mi, S = map(int, (m , m , m , m , m , m ))
    try:
        datetime(y, mo, d, H, Mi, S)
    except ValueError:
        return False, "invalid date/time"
    return True, "ok"


def parse(s):
    """Parse a T-Zero timestamp into a timezone-aware UTC datetime."""
    ok, msg = validate(s)
    if not ok:
        raise ValueError(msg)
    m = FMT.match(s)
    y, mo, d, H, Mi, S = map(int, (m , m , m , m , m , m ))
    ms = int((m or "0").ljust(3, "0"))
    return datetime(y, mo, d, H, Mi, S, ms * 1000, tzinfo=timezone.utc)


def fmt(dt):
    """Format a datetime as a T-Zero timestamp."""
    ms = dt.microsecond // 1000
    return dt.strftime("%Y%m%dT%H%M%S") + f".{ms:03d}"


def to_epoch_ms(s):
    """Convert a T-Zero timestamp to epoch milliseconds."""
    return int(parse(s).timestamp() * 1000)


def from_epoch_ms(ms):
    """Convert epoch milliseconds to a T-Zero timestamp."""
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return fmt(dt)


if __name__ == "__main__":
    tests = [
        ("20260926T154530.123", True),
        ("20260926T154530", True),
        ("20260926T154530.1", True),
        ("20260926T154530.12", True),
        ("20260230T120000", False),
        ("20260926 154530", False),
        ("20260926154530", False),
        ("20260926T256030", False),
        ("20260926T155060", False),
        ("20260926T154530.1234", False),
        ("20260926T154530.", False),
    ]
    for s, expect in tests:
        ok, msg = validate(s)
        status = "PASS" if ok == expect else "FAIL"
        print(f"{status}: {s!r} -> {ok} ({msg})")

    s = "20260926T154530.123"
    dt = parse(s)
    assert fmt(dt) == s
    assert from_epoch_ms(to_epoch_ms(s)) == s
    assert sorted(["20260926T154530.123", "20260926T154530.999"]) == [
        "20260926T154530.123",
        "20260926T154530.999",
    ]
    print("all self-tests passed")

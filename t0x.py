#!/usr/bin/env python3
"""T-Zero timestamp standard reference implementation.

Format: YYYYMMDDTHHMMSS.sss (exactly 19 characters, UTC, fixed-width)

Milliseconds are required and always three digits, left-padded with zeros
so the numeric millisecond value is 000–999 (.001 = 1ms, .100 = 100ms).
On input, 1–3 digit fractions are accepted and left-padded (.1 → .001, .12 → .012).
"""

import re
from datetime import datetime, timezone

FMT = re.compile(
    r"^(?P<y>\d{4})(?P<m>\d{2})(?P<d>\d{2})"
    r"T(?P<H>\d{2})(?P<M>\d{2})(?P<S>\d{2})"
    r"\.(?P<ms>\d{1,3})$"
)


def validate(s):
    """Return (True, 'ok') if s is a valid T-Zero timestamp, else (False, reason)."""
    m = FMT.match(s)
    if not m:
        return False, "format mismatch"
    y = int(m.group("y"))
    mo = int(m.group("m"))
    d = int(m.group("d"))
    H = int(m.group("H"))
    Mi = int(m.group("M"))
    S = int(m.group("S"))
    try:
        datetime(y, mo, d, H, Mi, S, tzinfo=timezone.utc)
    except ValueError:
        return False, "invalid date/time"
    return True, "ok"


def parse(s):
    """Parse a T-Zero timestamp into a timezone-aware UTC datetime."""
    ok, msg = validate(s)
    if not ok:
        raise ValueError(msg)
    m = FMT.match(s)
    y = int(m.group("y"))
    mo = int(m.group("m"))
    d = int(m.group("d"))
    H = int(m.group("H"))
    Mi = int(m.group("M"))
    S = int(m.group("S"))
    # Left-pad: .1 → 001 (1ms). Do not right-pad (.1 must not become 100).
    ms = int(m.group("ms").zfill(3))
    return datetime(y, mo, d, H, Mi, S, ms * 1000, tzinfo=timezone.utc)


def format(dt):
    """Format a datetime as a canonical 19-character T-Zero timestamp (UTC)."""
    if dt.tzinfo is None:
        raise ValueError("datetime must be timezone-aware (UTC)")
    dt = dt.astimezone(timezone.utc)
    ms = dt.microsecond // 1000
    return dt.strftime("%Y%m%dT%H%M%S") + f".{ms:03d}"


# Back-compat alias
fmt = format


def to_epoch_ms(s):
    """Convert a T-Zero timestamp to epoch milliseconds."""
    return int(parse(s).timestamp() * 1000)


def from_epoch_ms(ms):
    """Convert epoch milliseconds to a canonical T-Zero timestamp."""
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return format(dt)


if __name__ == "__main__":
    tests = [
        ("20260926T154530.123", True),
        ("20260926T154530.001", True),
        ("20260926T154530.1", True),
        ("20260926T154530.12", True),
        ("20260926T154530", False),
        ("20260926T154530.", False),
        ("20260230T120000.000", False),
        ("20260926 154530.000", False),
        ("20260926154530.000", False),
        ("20260926T256030.000", False),
        ("20260926T155060.000", False),
        ("20260926T154530.1234", False),
    ]
    for s, expect in tests:
        ok, msg = validate(s)
        status = "PASS" if ok == expect else "FAIL"
        print(f"{status}: {s!r} -> {ok} ({msg})")

    assert parse("20260926T154530.1").microsecond == 1000
    assert parse("20260926T154530.12").microsecond == 12000
    assert parse("20260926T154530.100").microsecond == 100000
    s = "20260926T154530.123"
    dt = parse(s)
    assert format(dt) == s
    assert len(format(dt)) == 19
    assert from_epoch_ms(to_epoch_ms(s)) == s
    assert sorted(
        ["20260926T154530.999", "20260926T154530.123", "20260926T154530.001"]
    ) == [
        "20260926T154530.001",
        "20260926T154530.123",
        "20260926T154530.999",
    ]
    print("all self-tests passed")

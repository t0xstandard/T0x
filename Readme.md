# t0x
# T-Zero Timestamp Standard

**https://t0x.dev**

A fixed-width, unambiguous timestamp format for cross-vendor data exchange.

## Format
YYYYMMDDTHHMMSS.sss

Exactly nineteen characters. Fixed-width. No delimiters except the `T` separator and the dot before milliseconds.

| Field | Digits | Range |
|---|---|---|
| Year | 4 | 0000-9999 |
| Month | 2 | 01-12 |
| Day | 2 | 01-31 (valid per month) |
| T | 1 | literal separator |
| Hour | 2 | 00-23 |
| Minute | 2 | 00-59 |
| Second | 2 | 00-59 |
| Dot | 1 | literal separator |
| Milliseconds | 3 | 000-999 (required) |

## Rules

1. **UTC only.** No timezone offsets. All timestamps are UTC.
2. **Zero-padded.** Every field is exactly its width. No spaces.
3. **Milliseconds required.** Always three digits, left-padded with zeros. `20260926T154530.001` is 1ms; `20260926T154530.100` is 100ms. On input, shorter fractions may be left-padded (`20260926T154530.1` → `.001`, `20260926T154530.12` → `.012`). Emitters must always write three digits.
4. **No trailing dot.** `20260926T154530.` is invalid. Omitting milliseconds entirely (`20260926T154530`) is invalid.
5. **Chronological sort.** Plain ASCII string sort equals chronological order. No parsing needed. This holds because the form is fixed-width and milliseconds are always three digits in the canonical encoding.

## Why

- **Unambiguous across locales.** Year-month-day ordering eliminates the month/day flip that plagues `MM/DD/YYYY` vs `DD/MM/YYYY`.
- **Fixed-width.** Every field sits at a known byte offset. Truncation shifts the `T` or the millisecond field and fails validation immediately.
- **ASCII-safe.** The `T` separator survives legacy systems, plain-text logs, and pipelines that strip non-ASCII characters.
- **Sortable.** String comparison gives you time order for free when values are stored in canonical 19-character form.

## Examples

```
20260926T154530.123
20260926T154530.001
20260926T000000.000
```

## Validation

A timestamp is valid if and only if:

- It matches the regex `^\d{8}T\d{6}\.\d{1,3}$` (parsers left-pad ms to three digits)
- Canonical emitted form matches `^\d{8}T\d{6}\.\d{3}$` (exactly 19 characters)
- The date portion is a real calendar date (no Feb 30)
- Hour is 00-23, minute and second are 00-59
- The value is interpreted as UTC

## Reference Implementation

See `t0x.py` in this repository. It provides `validate`, `parse`, `format`, `to_epoch_ms`, and `from_epoch_ms`.

## Contact
t0x Time Keeper
t0xstandard@gmail.com

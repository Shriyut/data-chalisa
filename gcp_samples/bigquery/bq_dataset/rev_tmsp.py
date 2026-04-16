import datetime

def reversed_timestamp(ts_str):
    # Parse the ISO timestamp
    dt = datetime.datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    # Convert to milliseconds since epoch
    epoch = datetime.datetime(1970, 1, 1)
    ms = int((dt - epoch).total_seconds() * 1000)
    # Use 13-digit max for Bigtable (ms precision)
    MAX_TS = 2**63 - 1
    reversed_ts = MAX_TS - ms
    return str(reversed_ts)

# Example usage
ts = "2026-01-29T20:30:44.892Z"
print(reversed_timestamp(ts))
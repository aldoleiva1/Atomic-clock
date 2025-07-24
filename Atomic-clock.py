import requests
import datetime
import socket
import time

TIME_ZONE = "America/Chicago"


def fetch_time(timezone: str):
    """Fetch the current time from timeapi.io with a DNS fallback."""
    base_url = "https://timeapi.io/api/time/current/zone"
    params = {"timeZone": timezone}
    try:
        resp = requests.get(base_url, params=params, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException:
        try:
            ip = socket.gethostbyname("timeapi.io")
            ip_url = f"https://{ip}/api/time/current/zone"
            headers = {"Host": "timeapi.io"}
            resp = requests.get(ip_url, params=params, headers=headers, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Error fetching time: {e}")
            return None


def atomic_clock():
    data = fetch_time(TIME_ZONE)
    if not data:
        return None
    timestamp = data.get("dateTime")
    if not timestamp:
        print("Unexpected response")
        return None
    return datetime.datetime.fromisoformat(timestamp)


if __name__ == "__main__":
    while True:
        current_time = atomic_clock()
        if current_time:
            print(current_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
        time.sleep(1)

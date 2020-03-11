import datetime
import json

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def cache_data(html, last_updated):
    with open("db.json", "w") as f:
        f.write(
            json.dumps(
                {
                    "html": html,
                    "last_updated": last_updated,
                    "updated_at": datetime.datetime.now().strftime(DATE_TIME_FORMAT),
                }
            )
        )


def get_cache():
    try:
        with open("db.json", "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return None


def get_cache_if_recent():
    cached_data = get_cache()
    if not cached_data:
        return None
    updated_at = datetime.datetime.strptime(cached_data["updated_at"], DATE_TIME_FORMAT)
    if updated_at < datetime.datetime.now() - datetime.timedelta(minutes=5):
        return None
    return cached_data

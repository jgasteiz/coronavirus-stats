import datetime
import json

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def cache_data(html_table, last_updated):
    with open("db.json", "w") as f:
        f.write(
            json.dumps(
                {
                    "html_table": html_table,
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


def is_cache_recent():
    cached_data = get_cache()
    if not cached_data:
        return False
    updated_at = datetime.datetime.strptime(cached_data["updated_at"], DATE_TIME_FORMAT)
    if updated_at < datetime.datetime.now() - datetime.timedelta(minutes=5):
        return False
    return True

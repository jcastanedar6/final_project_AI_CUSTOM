class ContextStore:
    def __init__(self):
        self._data = {}  # {user_id: {key: value}}

    def save(self, user_id, key, value):
        if user_id not in self._data:
            self._data[user_id] = {}
        self._data[user_id][key] = value
        return True

    def list_for_user(self, user_id):
        items = self._data.get(user_id, {})
        return [{"key": k, "value": v} for k, v in items.items()]

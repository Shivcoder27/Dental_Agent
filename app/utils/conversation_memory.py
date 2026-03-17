memory_store = {}


def save_message(user_id, message):

    if user_id not in memory_store:
        memory_store[user_id] = []

    memory_store[user_id].append(message)

    memory_store[user_id] = memory_store[user_id][-5:]


def get_history(user_id):

    return memory_store.get(user_id, [])
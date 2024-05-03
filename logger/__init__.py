
def logger_dict(key, obj):
    if str(key) in dict(obj):
        return f'{key}: {obj[str(key)]}'
    return f'Don\'t have key {key} in obj'

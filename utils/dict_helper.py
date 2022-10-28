def exclude_by_keys(exclude_keys: set[str], origin_data: dict) -> dict:
    extract_keys = set(origin_data.keys()) - exclude_keys
    return {key: origin_data.get(key, None) for key in extract_keys}

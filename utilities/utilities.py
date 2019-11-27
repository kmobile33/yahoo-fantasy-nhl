def safe_cast(val, to_type, default=None):
    """Cast to specified type. If casting fails, return a default value"""
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

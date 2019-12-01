def merge_if_not_none(session, entity):
    if entity is None:
        return None
    
    return session.merge(entity)

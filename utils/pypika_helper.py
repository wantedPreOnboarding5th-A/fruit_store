def dict_fetchone(cursor, is_lower: bool = True):
    desc = cursor.description
    data = cursor.fetchone()
    return (
        data
        if data == None
        else dict(
            zip(
                [col[0].lower() if is_lower else col[0] for col in desc],
                data,
            )
        )
    )

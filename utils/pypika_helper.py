from exceptions import NoResultToRetrieveRowCountError, TooManyCursorResult


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


def dict_fetchall(cursor, fetch_size_expected: int = 10000, is_lower: bool = True):
    # https://stackoverflow.com/questions/10888844/using-dict-cursor-in-django
    # Returns all rows from a cursor as a dict

    row_cnt = cursor.rowcount
    if row_cnt is None or row_cnt == -1:
        # https://peps.python.org/pep-0249/#rowcount
        raise NoResultToRetrieveRowCountError()
    elif row_cnt > fetch_size_expected:
        raise TooManyCursorResult()
    else:
        desc = cursor.description
        return [
            dict(zip([col[0].lower() if is_lower else col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

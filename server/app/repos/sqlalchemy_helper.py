def choose_columns(table, *columns):
    result = []
    for column in columns:
        if isinstance(column, str):
            result.append(table.c[column])
        elif isinstance(column, (tuple, list)):
            result.append(table.c[column[0]].label(column[1]))
        else:
            raise TypeError('Not supported type "{}"'.format(column))
    return result

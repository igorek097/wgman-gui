def get_values_list(queryset, field):
    if not queryset.count():
        return []
    values_qs = queryset.values_list(field)
    values_list = [i[0] for i in values_qs]
    return values_list


def write_to_file(file_path:str, data:str):
    with open(file_path, 'w') as f:
        f.write(data)
        
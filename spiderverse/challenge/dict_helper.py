def get_key( dictionary , lookup_value ):
    for key,val in dictionary.items():
        if val == lookup_value:
            return key
    return False
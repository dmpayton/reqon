def dict_in(value):
    '''
        Checks for the existence of a dictionary in a list

        Arguments:
        value -- A list

        Returns:
        A Boolean
    '''
    for item in value:
        if isinstance(item, dict):
            return True
    return False

def dict_in(value):
    '''
        Checks for the existence of a dictionary in a list

        Arguments:
        value -- A list

        Returns:
        A Boolean
    '''
    return any(isinstance(item, dict) for item in value)

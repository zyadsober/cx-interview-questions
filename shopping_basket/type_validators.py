def validate_type(instance, expected_type):
    if not isinstance(instance, expected_type):
        raise TypeError('expected {} but found {} instead'.format(
                                                type(expected_type).__name__,
                                                type(instance).__name__))

def validate_list_type_and_children_types(instance, children_expected_type):
    if not isinstance(instance, list):
        raise TypeError('expected list type for products but '
                            'found {} instead'.format(type(instance).__name__))
    for item in instance:
        validate_type(item, children_expected_type)

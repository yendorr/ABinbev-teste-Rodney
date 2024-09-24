# products/utils.py

from bson import ObjectId

def convert_objectid_to_str(data):
    """
    Recursively converts ObjectId instances to their string representations in dictionaries, lists, or individual values.

    Args:
        data (Any): The data to be processed. Can be a single value, list, or dictionary. If it's an ObjectId, it will be converted to a string.

    Returns:
        Any: The same data structure with all ObjectId instances replaced by their string representations.

    Raises:
        KeyError: If there is an error accessing dictionary keys.
    """
    
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    return data
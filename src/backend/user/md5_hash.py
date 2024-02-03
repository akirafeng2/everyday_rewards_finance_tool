import hashlib


def hash_string_md5(input_string):
    # Create a new MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the bytes of the input string
    md5_hash.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_string = md5_hash.hexdigest()

    return hashed_string

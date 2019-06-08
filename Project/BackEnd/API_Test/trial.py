def decrypt_private_data(private_data_base64_string, encryption_key):
    """Takes the base64 encoded private data string (private_data field from private_data_object).
     Will attempt to recreate the same secret box and decrypt using the provided encryption key."""
    try:
        status, secret_box = create_secret_box(encryption_key)
        if not status:
            return False, None
        # convert the string back to base64 bytes.
        private_data_base64_bytes = private_data_base64_string.encode('utf-8')
        # Decode the base64 bytes to get back the encrypted message object.
        received_encrypted_message_object = base64.b64decode(private_data_base64_bytes)

        # Decrypt the encrypted message object with the receiving secret box.
        unencrypted_bytes = secret_box.decrypt(received_encrypted_message_object)
        # Convert the bytes back to a string, then to a dictionary.
        unencrypted_string = unencrypted_bytes.decode('utf-8')
        private_data_dict = json.loads(unencrypted_string)
        print("This is the private data that was retrieved:")
        pprint.pprint(private_data_dict)
        return True, private_data_dict
    except nacl.exceptions.CryptoError:
        return False, None
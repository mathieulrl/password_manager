from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import tink
from tink import daead, cleartext_keyset_handle

app = Flask(__name__)
CORS(app)

# def generate_aes_siv_key():
#     daead.register()
#     key_template = daead.deterministic_aead_key_templates.AES256_SIV
#     keyset_handle = tink.new_keyset_handle(key_template)
#     with open('aes_siv_key.json', 'wt') as keyset_file:
#         cleartext_keyset_handle.write(tink.JsonKeysetWriter(keyset_file), keyset_handle)
# generate_aes_siv_key()

def init_tink_deterministic():
    daead.register()
    keyset = r"""{
    "key": [{
        "keyData": {
            "keyMaterialType":
                "SYMMETRIC",
            "typeUrl":
                "type.googleapis.com/google.crypto.tink.AesSivKey",
            "value":
                "EkAobOz+mL3XphMYHgMKitKTDANm69aQe0tgN82uYhT1tW07Q74fuyy7MoHN+WrZVvfTfCho5vC0Ai5d9nIa3exf"
        },
        "outputPrefixType": "TINK",
        "status": "ENABLED"
    }]
}"""
    keyset_handle = cleartext_keyset_handle.read(tink.JsonKeysetReader(keyset))
    return keyset_handle

KEYSET_HANDLE = init_tink_deterministic()

def encrypt_deterministic(plaintext, associated_data):
    daead_primitive = KEYSET_HANDLE.primitive(daead.DeterministicAead)
    return daead_primitive.encrypt_deterministically(plaintext, associated_data)

import base64

@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Retrieve the hash from the request
    hash_value = request.json.get('hashed_password')

    # Check if the hash is provided
    if hash_value:
        encrypted_password = encrypt_deterministic(hash_value.encode('utf-8'), b'')
        encrypted_password_b64 = base64.b64encode(encrypted_password).decode('utf-8')
        # Return the encrypted hash as JSON response
        return jsonify({'encrypted_hash': encrypted_password_b64})

    # Return an error message if no hash is provided
    return jsonify({'error': 'No hash provided'}), 400

if __name__ == '__main__':
    app.run(port=3000)
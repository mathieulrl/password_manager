from flask import Flask, request, jsonify
from tink import aead
from tink import new_keyset_handle

app = Flask(__name__)

# Initialize Tink
aead.register()

# Generate the keyset
key_template = aead.aead_key_templates.AES256_GCM
keyset_handle = new_keyset_handle(key_template)



@app.route('/encrypt', methods=['POST'])
def encrypt():
    hash_value = request.json.get('hashed_password')
    print(hash_value)
    if hash_value:
        try:
            # Get the AEAD primitive
            aead_primitive = keyset_handle.primitive(aead.Aead)
            print(aead_primitive)
            # Encryption
            encrypted_hash = aead_primitive.encrypt(hash_value.encode(), b'')

            return jsonify({'encrypted_hash': encrypted_hash})

        except Exception as e:
            print(str(e))
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'No hash provided'}), 400


if __name__ == '__main__':
    app.run(port=3000)
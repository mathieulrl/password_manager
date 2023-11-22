from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet

app = Flask(__name__)
CORS(app)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    # Retrieve the hash from the request
    hash_value = request.json.get('hashed_password')

    # Check if the hash is provided
    if hash_value:
        # Generate encryption key
        key = Fernet.generate_key()
        f = Fernet(key)

        # Encrypt the hash
        encrypted_hash = f.encrypt(hash_value.encode())

        # Return the encrypted hash as JSON response
        return jsonify({'encrypted_hash': encrypted_hash.decode()})

    # Return an error message if no hash is provided
    return jsonify({'error': 'No hash provided'}), 400

if __name__ == '__main__':
    app.run(port=3000)
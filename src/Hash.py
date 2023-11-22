from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import requests
import csv

app = Flask(__name__)
CORS(app)

@app.route('/encrypt', methods=['POST'])
def hash():
    username = request.form.get('username')
    password = request.form.get('password')
    print("username:", username)
    print("password: ",password)

    # Vérifier si le mot de passe a été envoyé
    if username is not None and password is not None:
        # Convertir le mot de passe en bytes
        password_bytes = password.encode('utf-8')

        # Créer un objet de hachage SHA-256
        hasher = hashlib.sha256()

        # Mettre à jour le hachage avec les bytes du mot de passe
        hasher.update(password_bytes)

        # Récupérer le hachage final en hexadecimal
        hash_password = hasher.hexdigest()
        print("hash_password:",hash_password)

        # Send the hashed password to another port (e.g., port 5002)
        other_port_url = 'http://localhost:3001/encrypt'  # Update with the desired URL
        payload = {'hashed_password': hash_password}
        response = requests.post(other_port_url, json=payload)

        if response.status_code == 200:
            encrypted_hash = response.json().get('encrypted_hash')
            print("encrypted_hash:", encrypted_hash)

            # Write to CSV
            with open('passwords.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password, encrypted_hash])
            return jsonify({'message': 'Hashed and encrypted password stored successfully'})
        
        else:
            return jsonify({'error': 'Encryption server error'}), 500
        
    else:
        return jsonify({'error': 'No password provided'}), 400

if __name__ == '__main__':
    app.run()
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import requests
import csv
import os

app = Flask(__name__)
CORS(app)

@app.route('/hash', methods=['POST'])
def hash():
    username = request.form.get('username')
    password = request.form.get('password')
    print("username:", username)
    print("password: ",password)

    # Vérifier si le mot de passe a été envoyé
    if username is not None and password is not None:
        # Generate a salt
        salt = os.urandom(16)
        salt_hex = salt.hex()  # Convert salt to hexadecimal for storage

        # Convert the password and salt to bytes and concatenate
        password_bytes = (salt + password.encode('utf-8'))

        # Créer un objet de hachage SHA-256
        hasher = hashlib.sha256()
        # Mettre à jour le hachage avec les bytes du mot de passe
        hasher.update(password_bytes)
        # Récupérer le hachage final en hexadecimal
        hash_password = hasher.hexdigest()
        print("hash_password:",hash_password)

        # Send the hashed password to be encrypted
        other_port_url = 'http://localhost:3000/encrypt'  
        payload = {'hashed_password': hash_password} #Create the json
        response = requests.post(other_port_url, json=payload) # Send the json to the other port

        if response.status_code == 200:
            encrypted_hash = response.json().get('encrypted_hash')
            print("encrypted_hash:", encrypted_hash)

            # Write to CSV
            with open('passwords.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, salt_hex, encrypted_hash])
            return jsonify({'message': 'Hashed and encrypted password stored successfully'})
        
        else:
            return jsonify({'error': 'Encryption server error'}), 500
        
    else:
        return jsonify({'error': 'No password provided'}), 400

# Function to verify if the entered password matches the stored hash
@app.route('/verify_password', methods=['POST'])
def verify_password():
    username = request.form.get('username')
    password = request.form.get('password')

    # Find the user's salt and stored encrypted password from the CSV file
    with open('passwords.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if (row[0] == username):
                stored_salt_hex = row[1] # the salt is stored in the second column
                stored_password = row[2]  # the hashed_encrypted password is stored in the third column

                # Convert the hex salt back to bytes
                stored_salt = bytes.fromhex(stored_salt_hex)
                # Concatenate the salt with the password and hash it
                password_bytes = (stored_salt + password.encode('utf-8'))
                hasher = hashlib.sha256()
                hasher.update(password_bytes)
                hash_password = hasher.hexdigest()
                # Send the hashed password to be encrypted
                other_port_url = 'http://localhost:3000/encrypt'  
                payload = {'hashed_password': hash_password} 
                response = requests.post(other_port_url, json=payload) 

                if response.status_code == 200:       
                    encrypted_hash = response.json().get('encrypted_hash')    

                    print("encrypted_hash:", encrypted_hash)
                    print("stored_password:", stored_password)
                    print("salt:", row[1])
                    print("stored_password == encrypted_hash:", stored_password == encrypted_hash)

                    if stored_password == encrypted_hash:
                        return jsonify({'message': 'Login Succeeded - Password matches'})
                    else:
                        return jsonify({'message': 'Login Failed - Password does not match'})
                else:
                    return jsonify({'error': 'Encryption server error'}), 500
        return jsonify({'message': 'Login Failed - Username not found'})


if __name__ == '__main__':
    app.run()

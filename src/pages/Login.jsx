import React from "react";
import { useState } from 'react';
import {Link, BrowserRouter as Router, Route, Routes} from 'react-router-dom';


function Login() {
  const [password, setPassword] = useState('')
  const [username, setUsername] = useState('')

  const handleUsernameChange = (event) => {
    setUsername(event.target.value)
  }

  const handlePasswordChange = (event) => {
    setPassword(event.target.value)
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
  
    // Envoyer le mot de passe pour vérification
    const response = await fetch('http://127.0.0.1:5000/verify_password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    });
  
    // Vérifier si la requête a réussi
    if (response.ok) {
      const result = await response.json();
      console.log('Response from server:', result.message);
    } else {
      console.error('Failed to hash password');
    }
  };

  return (
      <>
        <h1>Login</h1>
        <div className="card">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="username">Username: </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={handleUsernameChange}
                placeholder="Enter your username"
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password: </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={handlePasswordChange}
                placeholder="Enter your password"
              />
            </div>
            <button type="submit">Login</button>
          </form>
        </div>

        <div>
        <Link to="/">Sing In</Link>
        </div>
        </>
  );
}

export default Login;

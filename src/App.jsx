import { useState } from 'react'
import React from 'react';
import {Link, BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Login from './pages/Login'; 
import './App.css'

function App() {
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
  
    // Envoyer le mot de passe à l'API pour le hashage
    const response = await fetch('http://127.0.0.1:5000/hash', {
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
    <Router>
      <Routes>
      <Route exact path="/" element={<>
      <h1>Sign In</h1>
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
          <button type="submit">Submit</button>
        </form>
      </div>
      <div> 
        <Link to="/Login">Login</Link>
      </div>
      </>}/>
      <Route exact path="/Login" element={<Login/>} />
      </Routes>
    </Router>
  )
}

export default App

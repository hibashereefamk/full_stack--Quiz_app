import React from 'react'
import './Navbar.css'
import { useState } from 'react';
function Navbar() {
const [username, setUsername] = useState('Learner');
    const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  return (
    <nav className="navbar">
        <div className="logo">🧠 QuizMaster</div>
        <div className="nav-links">
          <span>Hello, {username}</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </nav>
  )
}

export default Navbar
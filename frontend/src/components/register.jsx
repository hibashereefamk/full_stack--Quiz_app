import { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import './register.css'; 

const Register = () => {
    
    const [formData, setFormData] = useState({
        name: '',     
        username: '',
        email: '',
        phone_number: '', 
        password: '',
        role: 'student' 
    });
    
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setError('');

        try {
            // Make sure this URL matches your Django urls.py
            await axios.post('http://127.0.0.1:8000/api/register/', formData);
            
            alert('Registration Successful! Please Login.');
            navigate('/login');
        } catch (err) {
            console.error("Registration error", err);
            if (err.response) {
                // Show the specific error from Django (like "Name required")
                setError(JSON.stringify(err.response.data)); 
            } else {
                setError('Registration failed. Server not reachable.');
            }
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-form">
                <h2>Create Account</h2>
                
                {error && <div className="error-msg">{error}</div>}

                <form onSubmit={handleRegister}>
                    
                    {/* --- 2. ADD INPUT FOR NAME (Required) --- */}
                    <div className="form-group">
                        <label>Full Name</label>
                        <input 
                            type="text" 
                            name="name" 
                            value={formData.name} 
                            onChange={handleChange} 
                            required 
                            placeholder="Enter your full name"
                        />
                    </div>

                    {/* --- 3. ADD INPUT FOR PHONE (Optional) --- */}
                    <div className="form-group">
                        <label>Phone Number</label>
                        <input 
                            type="text" 
                            name="phone_number" 
                            value={formData.phone_number} 
                            onChange={handleChange} 
                            placeholder="Enter phone number"
                        />
                    </div>

                    <div className="form-group">
                        <label>Username</label>
                        <input 
                            type="text" 
                            name="username" 
                            value={formData.username} 
                            onChange={handleChange} 
                            required 
                        />
                    </div>

                    <div className="form-group">
                        <label>Email</label>
                        <input 
                            type="email" 
                            name="email" 
                            value={formData.email} 
                            onChange={handleChange} 
                            required 
                        />
                    </div>

                    <div className="form-group">
                        <label>Password</label>
                        <input 
                            type="password" 
                            name="password" 
                            value={formData.password} 
                            onChange={handleChange} 
                            required 
                        />
                    </div>

                    <div className="form-group">
                        <label>I am a:</label>
                        <select name="role" value={formData.role} onChange={handleChange}>
                            <option value="student">Student</option>
                            <option value="teacher">Teacher</option>
                        </select>
                    </div>

                    <button type="submit" className="auth-button">Sign Up</button>
                </form>
                
                <div className="auth-link">
                    Already have an account? <Link to="/login">Login here</Link>
                </div>
            </div>
        </div>
    );
};

export default Register;
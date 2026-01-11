import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import './Home.css'; // Import the new CSS

const Home = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // 1. Check for token
    const token = localStorage.getItem('access_token');
    if (!token) {
        navigate('/login');
        return;
    }

    // 2. Fetch Categories (Not Questions!)
    // We need categories so the user can choose one to see the Quiz List
    axios.get('http://127.0.0.1:8000/categories/', {
      headers: {
        Authorization: `Bearer ${token}` 
      }
    })
      .then(response => {
        setCategories(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching categories:", error);
        setLoading(false);
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('access_token'); // Clear invalid token
            navigate('/login');
        }
      });
  }, [navigate]);

  

  const handleCategoryClick = (categoryId) => {
    // Navigate to the QuizListPage for this specific category
    navigate(`/category/${categoryId}`);
  };

  // Helper to give cards random colors or icons if your DB doesn't have them
  const getIcon = (name) => {
    const icons = {
      'Science': '🔬', 'Math': '📐', 'History': '📜', 'Coding': '💻', 'General': '🌍'
    };
    return icons[name] || '📚';
  };

  return (
    <div className="home-container">
      {/* Navbar Section */}
      

      {/* Hero Section */}
      <header className="hero">
        <h1>What do you want to learn today?</h1>
        <p>Select a category to view available quizzes and test your skills.</p>
      </header>
      
      {/* Content Section */}
      {loading ? (
        <div className="loader">Loading Categories...</div>
      ) : (
        <div className="category-grid">
          {categories.length === 0 ? (
             <p className="no-data">No categories available right now.</p>
          ) : (
            categories.map((cat) => (
              <div 
                key={cat.id} 
                className="category-card"
                onClick={() => handleCategoryClick(cat.id)}
              >
                <div className="cat-icon">{getIcon(cat.name)}</div>
                <h3>{cat.name}</h3>
                <p>Click to explore quizzes</p>
                <div className="arrow-btn">➜</div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default Home;
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './QuizListPage.css'; // Don't forget the CSS below

const QuizListPage = () => {
  const { categoryId } = useParams(); // Get ID from URL
  const navigate = useNavigate();

  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const token = localStorage.getItem('access_token');
        
        
        const response = await axios.get(
          `http://127.0.0.1:8000/quizzess/category/${categoryId}/`, 
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        setQuizzes(response.data);
        console.log(response.data)
      } catch (err) {
        console.error(err);
        setError("Failed to load quizzes.");
      } finally {
        setLoading(false);
      }
    };

    fetchQuizzes();
  }, [categoryId]);

  const handleStart = (quizId) =>{
    navigate(`/quiz/${quizId}`); // Go to the Quiz taking page
  };

  if (loading) return <div className="loading-spinner">Loading...</div>;
  if (error) return <div className="error-msg">{error}</div>;

  return (
    <div className="quiz-list-page">
      {/* Header Section */}
      <div className="page-header">
        <button onClick={() => navigate(-1)} className="back-btn">← Categories</button>
        <h1>Select a Quiz</h1>
      </div>

      <div className="quiz-list">
        {quizzes.length === 0 ? (
          <div className="no-quizzes">No quizzes found in this category.</div>
        ) : (
          quizzes.map((quiz) => (
            <div key={quiz.id} className={`quiz-card ${quiz.is_attempted ? 'attempted' : ''}`}>
              
              {/* Row 1: Title & Level */}
              <div className="card-top">
                <h3>{quiz.title}</h3>
                <span className={`level-badge ${quiz.level?.toLowerCase()}`}>
                    {quiz.level || 'Medium'}
                </span>
              </div>

              {/* Row 2: Stats (Questions & Time) */}
              <div className="card-stats">
                <div className="stat-item">
                  <span className="icon">❓</span>
                  <span>{quiz.questions_count} Questions</span>
                </div>
                <div className="stat-item">
                  <span className="icon">⏱️</span>
                  <span>{quiz.time_limit} Mins</span>
                </div>
              </div>

              {/* Row 3: Action Button */}
              <div className="card-action">
                {quiz.is_attempted ? (
                  <button className="btn-disabled" disabled>
                    ✅ Completed
                  </button>
                ) : (
                  <button 
                    className="btn-start" 
                    onClick={() => handleStart(quiz.id)}
                  >
                    Start Quiz
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default QuizListPage;
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './QuizPage.css'; // We will create this next

const QuizPage = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();

  // State
  const [quiz, setQuiz] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOptions, setSelectedOptions] = useState({}); // { questionId: optionId }
  const [timeLeft, setTimeLeft] = useState(0); // In seconds
  const [loading, setLoading] = useState(true);


  // 1. Fetch Quiz Data on Load
  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(`http://127.0.0.1:8000/quizzess/${quizId}/`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        
        setQuiz(response.data);
        // Convert minutes to seconds for the timer
        setTimeLeft(response.data.time_limit * 60); 
        setLoading(false);
      } catch (error) {
        console.error("Error fetching quiz:", error);
        alert("Failed to load quiz.");
        navigate(-1); // Go back if error
      }
    };
    fetchQuiz();
  }, [quizId, navigate]);

  // 2. Timer Logic
  useEffect(() => {
    if (!loading && timeLeft > 0) {
      const timerId = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
      return () => clearInterval(timerId);
    } else if (timeLeft === 0 && !loading) {
      // Auto-submit when time hits 0
      handleSubmit(); 
    }
  }, [timeLeft, loading]);

  // Helper: Format Time (e.g., 5:00)
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
  };

  // 3. Handle Option Selection
  const handleOptionSelect = (questionId, optionId) => {
    setSelectedOptions((prev) => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  // 4. Handle Next Button
  const handleNext = () => {
    if (currentQuestionIndex < quiz.questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1);
    }
  };

  // 5. Handle Previous Button
  const handlePrev = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex((prev) => prev - 1);
    }
  };

  // 6. Submit Quiz
  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      // Calculate missing/skipped questions if needed, or just send what we have
      const payload = {
        quiz_id: quizId,
        answers: selectedOptions
      };

      const response = await axios.post('http://127.0.0.1:8000/submit/', payload, {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Redirect to Result Page with the score data
      // You can pass the result via state to avoid re-fetching
      navigate('/result', { state: { resultData: response.data } });

    } catch (error) {
      console.error("Error submitting quiz:", error);
      alert("Error submitting quiz. Please try again.");
    }
  };

  if (loading) return <div className="loading">Loading Exam...</div>;

  // Get current question data
  const currentQuestion = quiz.questions[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === quiz.questions.length - 1;

  return (
    <div className="quiz-page-container">
      {/* Header: Title and Timer */}
      <div className="quiz-header">
        <h2>{quiz.title}</h2>
        <div className={`timer ${timeLeft < 60 ? 'warning' : ''}`}>
          ⏳ {formatTime(timeLeft)}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${((currentQuestionIndex + 1) / quiz.questions.length) * 100}%` }}
        ></div>
      </div>

      {/* Question Card */}
      <div className="question-card">
        <div className="question-count">
          Question {currentQuestionIndex + 1} of {quiz.questions.length}
        </div>
        
        <h3 className="question-text">{currentQuestion.text}</h3>

        <div className="options-grid">
          {currentQuestion.options.map((option) => (
            <div 
              key={option.id}
              className={`option-box ${selectedOptions[currentQuestion.id] === option.id ? 'selected' : ''}`}
              onClick={() => handleOptionSelect(currentQuestion.id, option.id)}
            >
              {option.text}
            </div>
          ))}
        </div>
      </div>

      {/* Navigation Buttons */}
      <div className="quiz-footer">
        <button 
          className="nav-btn prev" 
          onClick={handlePrev} 
          disabled={currentQuestionIndex === 0}
        >
          Previous
        </button>

        {isLastQuestion ? (
          <button className="nav-btn submit" onClick={handleSubmit}>
            Submit Quiz
          </button>
        ) : (
          <button className="nav-btn next" onClick={handleNext}>
            Next ➜
          </button>
        )}
      </div>
    </div>
  );
};

export default QuizPage;
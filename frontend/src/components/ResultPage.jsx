import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ResultPage.css';

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Get data passed from QuizPage
  const resultData = location.state?.resultData;

  if (!resultData) {
    return (
      <div className="result-container">
        <h2>No result found</h2>
        <button onClick={() => navigate('/')}>Go Home</button>
      </div>
    );
  }

  const { score, total_marks, percentage, results } = resultData;

  return (
    <div className="result-container">
      {/* Summary Card */}
      <div className="result-summary">
        <h2>Quiz Result</h2>
        <p><strong>Score:</strong> {score} / {total_marks}</p>
        <p><strong>Percentage:</strong> {percentage.toFixed(2)}%</p>

        <div className={`result-status ${percentage >= 40 ? 'pass' : 'fail'}`}>
          {percentage >= 40 ? '✅ Passed' : '❌ Failed'}
        </div>
      </div>

      {/* Detailed Question Results */}
      <div className="result-details">
        <h3>Answer Review</h3>

        {results.map((item, index) => (
          <div 
            key={index} 
            className={`result-question ${item.is_correct ? 'correct' : 'wrong'}`}
          >
            <h4>
              Q{index + 1}. {item.question}
            </h4>

            <p>
              <strong>Correct Answer:</strong> {item.correct_text}
            </p>

            <p>
              <strong>Status:</strong>{' '}
              {item.is_correct ? 'Correct ✅' : 'Wrong ❌'}
            </p>

            {item.explanation && (
              <p className="explanation">
                <strong>Explanation:</strong> {item.explanation}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* Actions */}
      <div className="result-actions">
        <button onClick={() => navigate('/')}>🏠 Home</button>
        <button onClick={() => navigate(-1)}>🔁 Retry</button>
      </div>
    </div>
  );
};

export default ResultPage;

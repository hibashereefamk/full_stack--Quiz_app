
import Login from './components/login'
import { Routes, Route } from "react-router-dom";
import Register from './components/register';
import Home from './components/Home';
import Navbar from './components/navbar';
import QuizListPage from './components/QuizListPage';
import QuizPage from './components/QuizPage';
import ResultPage from './components/ResultPage';
function App() {
  return (
  <>
    <Navbar/>
    <Routes>
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Home />} />
      <Route path='/category/:categoryId' element={<QuizListPage/>}/>
      <Route path='/result' element={<ResultPage/>}/>
      <Route path="/quiz/:quizId" element={<QuizPage />} />
    </Routes>
   
    </>
  )
}

export default App
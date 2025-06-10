import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  
  useEffect(() => {
    // Verificar si hay un token almacenado
    const token = localStorage.getItem('accessToken');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={
          !isAuthenticated ? 
          (showRegister ? 
            <Register setIsAuthenticated={setIsAuthenticated} setShowRegister={setShowRegister} /> :
            <Login setIsAuthenticated={setIsAuthenticated} setShowRegister={setShowRegister} />
          ) : 
          <Navigate to="/dashboard" />
        } />
        <Route path="/dashboard" element={
          isAuthenticated ? 
          <Dashboard setIsAuthenticated={setIsAuthenticated} /> : 
          <Navigate to="/login" />
        } />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;


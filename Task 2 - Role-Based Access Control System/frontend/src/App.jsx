// src/App.jsx

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import GuestPreview from './pages/GuestPreview';
import { Navbar, Nav, Container } from 'react-bootstrap';

function AppWrapper() {
  return (
    <Router>
      <App />
    </Router>
  );
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  // Check auth status on initial load
  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
    
    // If logged in but on sign-in page, redirect to dashboard
    if (token && window.location.pathname === '/') {
      navigate('/dashboard');
    }
  }, [navigate]);

  // Listen for storage changes
  useEffect(() => {
    const handler = () => {
      const token = localStorage.getItem('token');
      setIsLoggedIn(!!token);
      if (!token && window.location.pathname !== '/') {
        navigate('/');
      }
    };
    window.addEventListener('storage', handler);
    return () => window.removeEventListener('storage', handler);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    setIsLoggedIn(false);
    navigate('/');
  };

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg" className="shadow">
        <Container>
          <Navbar.Brand as={Link} to={isLoggedIn ? "/dashboard" : "/"}>RBAC System</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              {isLoggedIn ? (
                <>
                  <Nav.Link as={Link} to="/dashboard">Dashboard</Nav.Link>
                  <Nav.Link as={Link} to="/guest">Guest Preview</Nav.Link>
                  <Nav.Link onClick={handleLogout} style={{ cursor: 'pointer' }}>Logout</Nav.Link>
                </>
              ) : (
                <>
                  <Nav.Link as={Link} to="/">Sign In</Nav.Link>
                  <Nav.Link as={Link} to="/signup">Sign Up</Nav.Link>
                  <Nav.Link as={Link} to="/guest">Guest Preview</Nav.Link>
                </>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Container className="py-4">
        <Routes>
          <Route path="/" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/guest" element={<GuestPreview />} />
        </Routes>
      </Container>
    </>
  );
}

export default AppWrapper;
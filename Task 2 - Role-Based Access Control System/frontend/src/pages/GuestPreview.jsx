// src/pages/GuestPreview.jsx

import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';
import { Card, Form, Button, Alert } from 'react-bootstrap';
import { useLocation } from 'react-router-dom';

export default function GuestPreview() {
  const [token, setToken] = useState('');
  const [resource, setResource] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const location = useLocation();

  useEffect(() => {
    // Check for token in URL
    const params = new URLSearchParams(location.search);
    const urlToken = params.get('token');
    if (urlToken) {
      setToken(urlToken);
      handleViewResource(urlToken);
    }
    // Check for deleted message in state
    if (location.state && location.state.deleted) {
      setSuccess('Resource deleted successfully!');
    }
    // eslint-disable-next-line
  }, []);

  const fadeIn = useSpring({
    from: { opacity: 0 },
    to: { opacity: 1 },
  });

  const slideIn = useSpring({
    from: { transform: 'translateX(-20px)' },
    to: { transform: 'translateX(0)' },
  });

  const handleViewResource = async (viewToken) => {
    setError('');
    setResource(null);
    try {
      const res = await fetch(`http://localhost:8000/guests/access/${viewToken}`);
      if (!res.ok) throw new Error('Invalid or expired token');
      const data = await res.json();
      setResource(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    handleViewResource(token);
  };

  return (
    <animated.div style={fadeIn}>
      <Card className="shadow-sm" style={{ maxWidth: '500px', margin: '0 auto' }}>
        <Card.Body>
          <Card.Title className="text-center mb-4">Guest Resource Preview</Card.Title>
          {error && <Alert variant="danger">{error}</Alert>}
          {success && <Alert variant="success">{success}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Label>Guest Token</Form.Label>
              <Form.Control
                placeholder="Guest Token"
                value={token}
                onChange={e => setToken(e.target.value)}
                required
              />
            </Form.Group>
            <Button variant="primary" type="submit" className="w-100">
              View Resource
            </Button>
          </Form>
          {resource && (
            <animated.div style={slideIn} className="mt-4">
              <Card>
                <Card.Body>
                  <Card.Title>{resource.name}</Card.Title>
                  <Card.Text as="pre" className="p-3 bg-light rounded">
                    {resource.content}
                  </Card.Text>
                </Card.Body>
              </Card>
            </animated.div>
          )}
        </Card.Body>
      </Card>
    </animated.div>
  );
}
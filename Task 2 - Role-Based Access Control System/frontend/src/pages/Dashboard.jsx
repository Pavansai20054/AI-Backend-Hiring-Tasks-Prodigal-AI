// src/pages/Dashboard.jsx

import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';
import { Card, Form, Button, Alert, Tab, Tabs, Spinner, InputGroup, Modal, Table } from 'react-bootstrap';
import { useNavigate, useLocation } from 'react-router-dom';
import { FaTrash } from 'react-icons/fa';

export default function Dashboard() {
  const [orgName, setOrgName] = useState('');
  const [deptName, setDeptName] = useState('');
  const [resourceName, setResourceName] = useState('');
  const [resourceContent, setResourceContent] = useState('');
  const [message, setMessage] = useState('');
  const [key, setKey] = useState('org');
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('token');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const checkAuth = async () => {
      if (!token) {
        navigate('/', { state: { from: location, error: 'Please sign in to access the dashboard.' } });
        return;
      }
      try {
        const res = await fetch('http://localhost:8000/auth/me', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error('Invalid token');
        setLoading(false);
      } catch {
        localStorage.clear();
        navigate('/', { state: { from: location, error: 'Session expired. Please sign in again.' } });
      }
    };
    checkAuth();
  }, [token, navigate, location]);

  const fadeIn = useSpring({ from: { opacity: 0 }, to: { opacity: 1 } });

  const createOrg = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const res = await fetch('http://localhost:8000/orgs/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json', 
          Authorization: `Bearer ${token}` 
        },
        body: JSON.stringify({ name: orgName }),
      });
      if (res.ok) {
        setMessage('Organization created successfully!');
        setOrgName('');
        setKey('dept');
      } else {
        setMessage('Error creating organization');
      }
    } catch (err) {
      setMessage('Error creating organization');
    }
  };

  const createDept = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const res = await fetch('http://localhost:8000/depts/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json', 
          Authorization: `Bearer ${token}` 
        },
        body: JSON.stringify({ name: deptName, org_id: 1 }),
      });
      if (res.ok) {
        setMessage('Department created successfully!');
        setDeptName('');
      } else {
        setMessage('Error creating department');
      }
    } catch (err) {
      setMessage('Error creating department');
    }
  };

  const uploadResource = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const res = await fetch('http://localhost:8000/resources/', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json', 
          Authorization: `Bearer ${token}` 
        },
        body: JSON.stringify({ 
          name: resourceName, 
          content: resourceContent, 
          org_id: 1 
        }),
      });
      if (res.ok) {
        setMessage('Resource uploaded successfully!');
        setResourceName('');
        setResourceContent('');
      } else {
        setMessage('Error uploading resource');
      }
    } catch (err) {
      setMessage('Error uploading resource');
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <Spinner animation="border" variant="primary" />
      </div>
    );
  }

  return (
    <animated.div style={fadeIn}>
      <Card className="shadow-sm">
        <Card.Body>
          <Card.Title className="text-center mb-4">Dashboard</Card.Title>
          {message && <Alert variant={message.includes('Error') ? 'danger' : 'success'}>{message}</Alert>}
          <Tabs activeKey={key} onSelect={(k) => setKey(k)} className="mb-3">
            <Tab eventKey="org" title="Create Organization">
              <Form onSubmit={createOrg} className="mt-3">
                <Form.Group className="mb-3">
                  <Form.Label>Organization Name</Form.Label>
                  <Form.Control
                    placeholder="Organization Name"
                    value={orgName}
                    onChange={e => setOrgName(e.target.value)}
                    required
                  />
                </Form.Group>
                <Button variant="primary" type="submit">
                  Create Organization
                </Button>
              </Form>
            </Tab>
            <Tab eventKey="dept" title="Create Department">
              <Form onSubmit={createDept} className="mt-3">
                <Form.Group className="mb-3">
                  <Form.Label>Department Name</Form.Label>
                  <Form.Control
                    placeholder="Department Name"
                    value={deptName}
                    onChange={e => setDeptName(e.target.value)}
                    required
                  />
                </Form.Group>
                <Button variant="primary" type="submit">
                  Create Department
                </Button>
              </Form>
            </Tab>
            <Tab eventKey="resource" title="Upload Resource">
              <Form onSubmit={uploadResource} className="mt-3">
                <Form.Group className="mb-3">
                  <Form.Label>Resource Name</Form.Label>
                  <Form.Control
                    placeholder="Resource Name"
                    value={resourceName}
                    onChange={e => setResourceName(e.target.value)}
                    required
                  />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Resource Content</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    placeholder="Resource Content"
                    value={resourceContent}
                    onChange={e => setResourceContent(e.target.value)}
                    required
                  />
                </Form.Group>
                <Button variant="primary" type="submit">
                  Upload Resource
                </Button>
              </Form>
            </Tab>
            <Tab eventKey="roles" title="Manage Roles">
              <RoleManagement />
            </Tab>
            <Tab eventKey="sharing" title="Share Resources">
              <ResourceSharing />
            </Tab>
          </Tabs>
        </Card.Body>
      </Card>
    </animated.div>
  );
}

function RoleManagement() {
  const [users, setUsers] = useState([]);
  const [resources, setResources] = useState([]);
  const [selectedUser, setSelectedUser] = useState('');
  const [selectedResource, setSelectedResource] = useState('');
  const [selectedRole, setSelectedRole] = useState('viewer');
  const [message, setMessage] = useState('');

  useEffect(() => {
    async function fetchData() {
      try {
        const usersRes = await fetch('http://localhost:8000/users/org/1', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        const resourcesRes = await fetch('http://localhost:8000/resources/org/1', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setUsers(await usersRes.json());
        setResources(await resourcesRes.json());
      } catch (err) {
        setMessage('Error loading data');
      }
    }
    fetchData();
  }, []);

  const assignRole = async () => {
    setMessage('');
    try {
      const res = await fetch('http://localhost:8000/users/assign-role', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}` 
        },
        body: JSON.stringify({
          user_id: Number(selectedUser),
          resource_id: selectedResource ? Number(selectedResource) : null,
          role: selectedRole
        })
      });
      if (res.ok) {
        setMessage('Role assigned successfully!');
      } else {
        const errorData = await res.json();
        setMessage(errorData.detail || 'Error assigning role');
      }
    } catch (err) {
      setMessage('Error assigning role');
    }
  };

  return (
    <div className="mt-3">
      <Form>
        <Form.Group className="mb-3">
          <Form.Label>User</Form.Label>
          <Form.Select 
            value={selectedUser} 
            onChange={e => setSelectedUser(e.target.value)}
            required
          >
            <option value="">Select User</option>
            {users.map(user => (
              <option key={user.id} value={user.id}>
                {user.email} ({user.full_name})
              </option>
            ))}
          </Form.Select>
        </Form.Group>
        
        <Form.Group className="mb-3">
          <Form.Label>Resource (leave blank for organization-wide)</Form.Label>
          <Form.Select 
            value={selectedResource} 
            onChange={e => setSelectedResource(e.target.value)}
          >
            <option value="">Organization-wide</option>
            {resources.map(res => (
              <option key={res.id} value={res.id}>{res.name}</option>
            ))}
          </Form.Select>
        </Form.Group>
        
        <Form.Group className="mb-3">
          <Form.Label>Role</Form.Label>
          <Form.Select 
            value={selectedRole} 
            onChange={e => setSelectedRole(e.target.value)}
            required
          >
            <option value="viewer">Viewer</option>
            <option value="contributor">Contributor</option>
            <option value="manager">Manager</option>
            <option value="admin">Admin</option>
          </Form.Select>
        </Form.Group>
        
        <Button variant="primary" onClick={assignRole}>
          Assign Role
        </Button>
        
        {message && (
          <Alert 
            variant={message.includes('Error') ? 'danger' : 'success'} 
            className="mt-3"
          >
            {typeof message === 'object' ? (message.msg || JSON.stringify(message)) : message}
          </Alert>
        )}
      </Form>
    </div>
  );
}

function ResourceSharing() {
  const [resources, setResources] = useState([]);
  const [selectedResource, setSelectedResource] = useState('');
  const [canEdit, setCanEdit] = useState(false);
  const [expiresAt, setExpiresAt] = useState('');
  const [generatedLink, setGeneratedLink] = useState('');
  const [message, setMessage] = useState('');
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteToken, setDeleteToken] = useState('');
  const [deleteMessage, setDeleteMessage] = useState('');
  const [showAllModal, setShowAllModal] = useState(false);
  const [allResources, setAllResources] = useState([]);
  const [resourceToDelete, setResourceToDelete] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchResources() {
      try {
        const res = await fetch('http://localhost:8000/resources/org/1', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setResources(await res.json());
      } catch (err) {
        setMessage('Error loading resources');
      }
    }
    fetchResources();
  }, []);

  const generateLink = async () => {
    setMessage('');
    if (!selectedResource) {
      setMessage('Please select a resource');
      return;
    }
    try {
      const res = await fetch(`http://localhost:8000/guests/share/${selectedResource}`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}` 
        },
        body: JSON.stringify({
          can_edit: canEdit,
          expires_at: expiresAt || null
        })
      });
      if (res.ok) {
        const data = await res.json();
        const link = `http://localhost:5173/guest?token=${data.token}`;
        setGeneratedLink(link);
        setMessage('Link generated successfully!');
      } else {
        const errorData = await res.json();
        setMessage(errorData.detail || 'Error generating link');
      }
    } catch (err) {
      setMessage('Error generating link');
    }
  };

  const handleDeleteResource = async () => {
    setDeleteMessage('');
    try {
      const res = await fetch('http://localhost:8000/resources/delete-by-token', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
        body: JSON.stringify({ token: deleteToken })
      });
      const data = await res.json();
      if (data.success) {
        setDeleteMessage('Resource deleted successfully!');
        setDeleteToken('');
        setShowDeleteModal(false);
        // Refresh resources
        const resList = await fetch('http://localhost:8000/resources/org/1', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setResources(await resList.json());
        // Show success message in the main UI
        setMessage('Resource deleted successfully!');
      } else {
        setDeleteMessage(data.detail || 'Error deleting resource');
      }
    } catch (err) {
      setDeleteMessage('Error deleting resource');
    }
  };

  const fetchAllResources = async () => {
    try {
      const res = await fetch('http://localhost:8000/resources/all/org/1', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setAllResources(await res.json());
      setShowAllModal(true);
    } catch (err) {
      setMessage('Error loading all resources');
    }
  };

  const handleDeleteRow = (resource) => {
    setResourceToDelete(resource);
    setConfirmDelete(true);
  };

  const confirmDeleteResource = async () => {
    setDeleteMessage('');
    try {
      // Find guest link for this resource to get token
      const res = await fetch(`http://localhost:8000/guests/share/${resourceToDelete.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
        body: JSON.stringify({ can_edit: false })
      });
      const data = await res.json();
      const token = data.token;
      const delRes = await fetch('http://localhost:8000/resources/delete-by-token', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${localStorage.getItem('token')}` },
        body: JSON.stringify({ token })
      });
      const delData = await delRes.json();
      if (delData.success) {
        setAllResources(allResources.filter(r => r.id !== resourceToDelete.id));
        setConfirmDelete(false);
        setResourceToDelete(null);
        setMessage('Resource deleted successfully!');
      } else {
        setDeleteMessage(delData.detail || 'Error deleting resource');
      }
    } catch (err) {
      setDeleteMessage('Error deleting resource');
    }
  };

  return (
    <div className="mt-3">
      <Form>
        <Form.Group className="mb-3">
          <Form.Label>Resource</Form.Label>
          <Form.Select 
            value={selectedResource} 
            onChange={e => setSelectedResource(e.target.value)}
            required
          >
            <option value="">Select Resource</option>
            {resources.map(res => (
              <option key={res.id} value={res.id}>{res.name}</option>
            ))}
          </Form.Select>
        </Form.Group>
        
        <Form.Group className="mb-3">
          <Form.Check 
            type="checkbox" 
            label="Allow Editing" 
            checked={canEdit}
            onChange={e => setCanEdit(e.target.checked)}
          />
        </Form.Group>
        
        <Form.Group className="mb-3">
          <Form.Label>Expiration Date (optional)</Form.Label>
          <Form.Control 
            type="datetime-local" 
            value={expiresAt}
            onChange={e => setExpiresAt(e.target.value)}
          />
        </Form.Group>
        
        <Button variant="primary" onClick={generateLink} className="me-2">
          Generate Link
        </Button>
        <Button variant="danger" onClick={() => setShowDeleteModal(true)} className="me-2">
          Delete Resource
        </Button>
        <Button variant="secondary" onClick={fetchAllResources}>
          Check All Resources
        </Button>
        
        {message && (
          <Alert 
            variant={message.includes('Error') ? 'danger' : 'success'} 
            className="mt-3"
          >
            {typeof message === 'object' ? (message.msg || JSON.stringify(message)) : message}
          </Alert>
        )}
        
        {generatedLink && (
          <div className="mt-3">
            <Form.Label>Shareable Link</Form.Label>
            <InputGroup>
              <Form.Control 
                value={generatedLink} 
                readOnly 
                className="bg-light"
              />
              <Button 
                variant="outline-secondary" 
                onClick={() => {
                  navigator.clipboard.writeText(generatedLink);
                  setMessage('Link copied to clipboard!');
                }}
              >
                Copy
              </Button>
            </InputGroup>
            <small className="text-muted">
              Share this link with guests to provide access
            </small>
          </div>
        )}
      </Form>
      <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Delete Resource</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group className="mb-3">
            <Form.Label>Enter Token to Delete Resource</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter token"
              value={deleteToken}
              onChange={e => setDeleteToken(e.target.value)}
              required
            />
          </Form.Group>
          {deleteMessage && (
            <Alert variant={deleteMessage.includes('successfully') ? 'success' : 'danger'}>
              {typeof deleteMessage === 'object' ? (deleteMessage.msg || JSON.stringify(deleteMessage)) : deleteMessage}
            </Alert>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={handleDeleteResource} disabled={!deleteToken}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
      <Modal show={showAllModal} onHide={() => setShowAllModal(false)} size="xl" centered>
        <Modal.Header closeButton>
          <Modal.Title>All Resources</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>Organization</th>
                <th>Department</th>
                <th>Resource Name</th>
                <th>Content</th>
                <th>Role</th>
                <th>Expire Date</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              {allResources.map(resource => (
                <tr key={resource.id}>
                  <td>{resource.org_name}</td>
                  <td>{resource.dept_name}</td>
                  <td>{resource.resource_name}</td>
                  <td style={{ maxWidth: 200, overflow: 'auto' }}>{resource.content}</td>
                  <td>{resource.role}</td>
                  <td>{resource.expire_date}</td>
                  <td className="text-center">
                    <FaTrash style={{ cursor: 'pointer', color: 'red' }} onClick={() => handleDeleteRow(resource)} />
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowAllModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
      <Modal show={confirmDelete} onHide={() => setConfirmDelete(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Delete</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Are you sure you want to delete the resource "{resourceToDelete?.resource_name}"?
          {deleteMessage && (
            <Alert variant="danger" className="mt-2">{typeof deleteMessage === 'object' ? (deleteMessage.msg || JSON.stringify(deleteMessage)) : deleteMessage}</Alert>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setConfirmDelete(false)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={confirmDeleteResource}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}
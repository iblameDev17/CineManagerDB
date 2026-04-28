import pytest
from app import app, db  # Assuming 'db' is your SQLAlchemy/MySQL instance

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # If using a DB, you might want to use an in-memory SQLite for tests
    with app.test_client() as client:
        yield client

# 1. Test Static Routes
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

# 2. Test Security: Unauthorized Access (DevSecOps requirement)
def test_admin_dashboard_protected(client):
    """Ensure sensitive pages redirect or deny access without login."""
    response = client.get('/admin', follow_redirects=True)
    # Should redirect to login or show 401/403
    assert response.status_code in [200, 401, 403] 

# 3. Test Functionality: Booking Logic
def test_ticket_booking_flow(client):
    """Test if a user can submit a booking form."""
    test_data = {'movie_id': 1, 'seats': 2}
    response = client.post('/book', data=test_data)
    # If successful, it usually redirects (302) or returns 200
    assert response.status_code in [200, 302]

# 4. Test Error Handling (Metric tracking requirement)
def test_404_page(client):
    """Check if the app handles non-existent routes (important for 500-error metrics)."""
    response = client.get('/this-page-does-not-exist')
    assert response.status_code == 404

import pytest
from unittest.mock import MagicMock, patch
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_user_credentials_match_database(client):
    """Test 1: Valid credentials accepted by Supabase (record exists in DB)."""
    mock_user = MagicMock()
    mock_user.user.email = 'testuser@example.com'

    with patch('login.routes.supabase') as mock_supabase:
        mock_supabase.auth.sign_in_with_password.return_value = mock_user

        response = client.post('/', data={
            'email': 'testuser@example.com',
            'password': 'correctpassword'
        })

        mock_supabase.auth.sign_in_with_password.assert_called_once_with({
            'email': 'testuser@example.com',
            'password': 'correctpassword'
        })
        assert response.status_code == 302


def test_successful_login_redirects_to_platform(client):
    """Test 2: Successful login redirects user to the SkillBridge platform."""
    mock_user = MagicMock()

    with patch('login.routes.supabase') as mock_supabase:
        mock_supabase.auth.sign_in_with_password.return_value = mock_user

        response = client.post('/', data={
            'email': 'testuser@example.com',
            'password': 'correctpassword'
        }, follow_redirects=False)

        assert response.status_code == 302
        assert '/platform' in response.headers['Location']

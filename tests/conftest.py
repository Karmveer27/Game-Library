import pytest

from games import MemoryRepository, create_app
from games.adapters import memory_repository
from utils import get_project_root

TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo

@pytest.fixture
def client():
    # Create your Flask app with testing configurations
    my_app = create_app({
        'TESTING': True,              # Set to True during testing.
        'REPOSITORY': 'memory',
        'TEST_DATA_PATH': TEST_DATA_PATH,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False     # test_client will not send a CSRF token, so disable validation.
    })

    # Return the test client instance for use in tests
    with my_app.test_client() as client:
        yield client

# Define an AuthenticationManager class for your authentication tests
class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register_user(self, user_name, password):
        return self.__client.post(
            '/authentication/register',
            data={'user_name': user_name, 'password': password}
        )

    def login(self, user_name='thorke', password='cLQ^C#oFXloS'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')

# Create an 'auth' fixture for authentication tests
@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
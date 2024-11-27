import logging
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from neo4j import GraphDatabase
from neomodel import config
from src.core.config import settings
from src.main import app

from tests.utils.utils import populate_database

logger = logging.getLogger(__name__)

config.DATABASE_URL = settings.DATABASE_URL


@pytest.fixture(scope='session')
def db_connection():
    """Create a Neo4j database connection that can be used throughout the tests."""
    uri = 'bolt://localhost:7687'
    auth = ('neo4j', '1234')  # username, password

    try:
        driver = GraphDatabase.driver(uri, auth=auth)
        driver.verify_connectivity()
        logger.info(f'Connected to Neo4j at {driver.get_server_info().address}')
        yield driver
    except Exception as e:
        logger.error(f'Failed to connect to Neo4j: {e}')
        raise
    finally:
        driver.close()


@pytest.fixture
def db_session(db_connection):
    with db_connection.session() as session:
        yield session


@pytest.fixture(autouse=True)
def cleanup(db_connection):
    """Automatically clean up after each test."""
    yield
    with db_connection.session() as session:
        session.run('MATCH (n) DETACH DELETE n')


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_tree(db_session):
    JSON_DATA = {
        'data': [
            {'name': 'A', 'description': 'This is a description of A', 'parent': ''},
            {'name': 'B', 'description': 'This is a description of B', 'parent': 'A'},
            {'name': 'C', 'description': 'This is a description of C', 'parent': 'A'},
            {'name': 'D', 'description': 'This is a description of D', 'parent': 'A'},
            {'name': 'B-1', 'description': 'This is a description of B-1', 'parent': 'B'},
            {'name': 'B-2', 'description': 'This is a description of B-2', 'parent': 'B'},
            {'name': 'B-3', 'description': 'This is a description of B-3', 'parent': 'B'},
        ]
    }
    return populate_database(JSON_DATA)

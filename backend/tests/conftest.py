import logging
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from neo4j import GraphDatabase
from src.main import app

logger = logging.getLogger(__name__)


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

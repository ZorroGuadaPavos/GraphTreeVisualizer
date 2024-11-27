from fastapi.testclient import TestClient
from src.core.config import settings


def test_get_all_tree_ids(client: TestClient, db_session, sample_tree):
    tree, nodes = sample_tree
    response = client.get(f'{settings.API_V1_STR}/trees/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert tree.uid in response.json()


def test_read_tree(client: TestClient, db_session, sample_tree):
    tree, nodes = sample_tree
    response = client.get(f'{settings.API_V1_STR}/trees/{tree.uid}')
    assert response.status_code == 200
    data = response.json()

    assert data['id'] == nodes['A']
    assert data['name'] == 'A'

    assert len(data['children']) == 3
    child_names = ['B', 'C', 'D']
    for child in data['children']:
        assert child['name'] in child_names
        assert child['id'] in [nodes[name] for name in child_names]


def test_read_tree_not_found(client: TestClient):
    response = client.get(f'{settings.API_V1_STR}/trees/nonexistent_id')
    assert response.status_code == 404
    assert response.json()['detail'] == 'tree not found'


def test_read_node(client: TestClient, db_session, sample_tree):
    tree, nodes = sample_tree
    # Test root node
    response = client.get(f'{settings.API_V1_STR}/trees/{tree.uid}/nodes/{nodes['A']}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == nodes['A']
    assert data['name'] == 'A'
    assert data['label'] == 'This is a description of A'

    # Test a child node
    response = client.get(f'{settings.API_V1_STR}/trees/{tree.uid}/nodes/{nodes['B']}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == nodes['B']
    assert data['name'] == 'B'
    assert data['label'] == 'This is a description of B'


def test_read_node_not_found(client: TestClient, db_session, sample_tree):
    tree, nodes = sample_tree
    response = client.get(f'{settings.API_V1_STR}/trees/{tree.uid}/nodes/nonexistent_id')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Node not found'

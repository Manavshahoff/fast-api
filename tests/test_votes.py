import pytest
from app import schemas, models
from app.config import settings

@pytest.fixture
def test_vote(test_user, session, test_posts):
    votes = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(votes)
    session.commit()

def test_vote_post(authorized_client, test_posts, test_user):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert response.status_code == 201

def test_vote_post_twice(authorized_client, test_posts, test_user):
    post_id = test_posts[3].id
    response = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    assert response.status_code == 201

    response = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    assert response.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_user):
    post_id = test_posts[0].id
    response = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 1})
    assert response.status_code == 201

    response = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 0})
    assert response.status_code == 201

def test_delete_nonexistent_vote(authorized_client, test_posts, test_user):
    post_id = test_posts[0].id
    response = authorized_client.post("/vote/", json={"post_id": post_id, "dir": 0})
    assert response.status_code == 404

def test_vote_nonexistent_post(authorized_client, test_user):
    response = authorized_client.post("/vote/", json={"post_id": 888888, "dir": 1})
    assert response.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    response = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert response.status_code == 401
import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, response.json())
    validated_posts = list(posts_map)
    assert response.status_code == 200
    assert len(validated_posts) == len(test_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/888888")
    assert response.status_code == 404

def test_get_one_post_wrong_user(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("new title", "new content", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.owner_id == test_user['id'] 
    assert created_post.published == published

def test_create_post_default_published(authorized_client, test_user):
    response = authorized_client.post("/posts/", json={"title": "new title", "content": "new content"})
    created_post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == "new title"
    assert created_post.content == "new content"
    assert created_post.owner_id == test_user['id'] 
    assert created_post.published == True

def test_unauthorized_user_create_post(client):
    response = client.post("/posts/", json={"title": "new title", "content": "new content"})
    assert response.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_not_exist(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/888888")
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts, test_user2):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert response.status_code == 403

def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.owner_id == test_user['id']

def test_update_post_not_exist(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": 888888,
    }
    response = authorized_client.put(f"/posts/888888", json=data)
    assert response.status_code == 404

def test_update_other_user_post(authorized_client, test_posts, test_user2, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403

def test_unauthorized_user_update_post(client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    response = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert response.status_code == 401
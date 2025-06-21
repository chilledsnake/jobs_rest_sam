def test_get_job(client):
    response = client.get(
        "/v1/info/",
    )
    assert response.text

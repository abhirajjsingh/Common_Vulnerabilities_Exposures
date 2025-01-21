import pytest
from app import app, init_db, get_db, fetch_and_store_cves

@pytest.fixture(scope="module")
def client():
    # Set up the Flask test client
    app.config['TESTING'] = True
    client = app.test_client()

    # Initialize the database and populate with test data
    init_db()
    fetch_and_store_cves(start_index=0, results_per_page=10)  # Insert test data
    yield client

    # Cleanup after the tests
    with app.app_context():
        db = get_db()
        db.execute("DELETE FROM cves")  # Clear the CVE table after tests
        db.commit()


# Test: Fetch CVEs with no filter
def test_get_cves_no_filter(client):
    response = client.get('/api/cves/filter')
    assert response.status_code == 200
    assert len(response.json) > 0  # Expecting some CVEs


# Test: Filter by CVSS score (min and max)
def test_filter_by_cvss_score(client):
    # Filter by min CVSS score
    response = client.get('/api/cves/filter?min_cvss=5')
    assert response.status_code == 200
    for cve in response.json:
        assert cve['cvss_score'] >= 5

    # Filter by max CVSS score
    response = client.get('/api/cves/filter?max_cvss=7')
    assert response.status_code == 200
    for cve in response.json:
        assert cve['cvss_score'] <= 7

    # Filter by min and max CVSS score
    response = client.get('/api/cves/filter?min_cvss=5&max_cvss=7')
    assert response.status_code == 200
    for cve in response.json:
        assert 5 <= cve['cvss_score'] <= 7


# Test: Filter by published date
def test_filter_by_published_date(client):
    # Filter by a specific published date (example: 2021-08-01)
    response = client.get('/api/cves/filter?published=2021-08-01')
    assert response.status_code == 200
    for cve in response.json:
        assert cve['published'] == '2021-08-01'


# Test: Filter by both published date and CVSS score
def test_filter_by_both(client):
    response = client.get('/api/cves/filter?published=2021-08-01&min_cvss=5')
    assert response.status_code == 200
    for cve in response.json:
        assert cve['published'] == '2021-08-01'
        assert cve['cvss_score'] >= 5


# Test: Filter with no matching results
def test_filter_no_match(client):
    response = client.get('/api/cves/filter?published=2025-01-01')
    assert response.status_code == 200
    assert len(response.json) == 0  # Expect no results for this date


if __name__ == "__main__":
    pytest.main()
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_business_branch_department_workflow():
    # Step 1: Create user A (business owner)
    user_a_data = {
        "email": f"test_owner_{uuid.uuid4()}@example.com",
        "password": "testpassword123",
        "is_active": True
    }
    response = client.post("/api/v1/users/", json=user_a_data)
    assert response.status_code == 201, f"Failed to create user: {response.json()}"
    user_a = response.json()
    user_a_id = user_a["id"]

    # Step 2: Log in as user A
    login_data = {
        "username": user_a_data["email"],
        "password": user_a_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, f"Failed to login as user A: {response.json()}"
    token_a = response.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # Step 3: Create business
    business_data = {
        "name": "Test Business",
        "description": "A test business",
        "email": "test@business.com",
        "phone": "1234567890",
        "address1": "123 Test St",
        "address2": "Suite 100",
        "city": "Test City",
        "state": "TS",
        "country": "Test Country",
        "postal_code": "12345",
        "website_url": "https://testbusiness.com",
        "is_active": True
    }
    response = client.post("/api/v1/businesses/", json=business_data, headers=headers_a)
    assert response.status_code == 201, f"Failed to create business: {response.json()}"
    business = response.json()
    business_id = business["id"]

    # Step 4: Create user C (branch manager)
    user_c_data = {
        "email": f"test_manager_{uuid.uuid4()}@example.com",
        "password": "testpassword123",
        "is_active": True
    }
    response = client.post("/api/v1/users/", json=user_c_data)
    assert response.status_code == 201, f"Failed to create user C: {response.json()}"
    user_c = response.json()
    user_c_id = user_c["id"]

    # Step 5: Log in as user C
    login_data = {
        "username": user_c_data["email"],
        "password": user_c_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, f"Failed to login as user C: {response.json()}"
    token_c = response.json()["access_token"]
    headers_c = {"Authorization": f"Bearer {token_c}"}

    # Step 6: Get or create a line of business to use for the branch
    response = client.get("/api/v1/line-of-business/", headers=headers_a)
    assert response.status_code == 200, f"Failed to get line of business: {response.json()}"
    lobs = response.json()
    if len(lobs) == 0:
        # Create a line of business
        lob_data = {
            "lob_name": f"Test LOB {uuid.uuid4()}",
            "is_active": True
        }
        response = client.post("/api/v1/line-of-business/", json=lob_data, headers=headers_a)
        assert response.status_code == 201, f"Failed to create line of business: {response.json()}"
        lob = response.json()
        lob_id = lob["id"]
    else:
        lob_id = lobs[0]["id"]

    # Step 7: Create branch
    # Generate a unique branch number and name to avoid conflict
    unique_id = str(uuid.uuid4())[:8]
    branch_number = 10000 + int(uuid.uuid4().int % 9000)  # between 10000 and 18999
    branch_data = {
        "name": f"Main Branch {unique_id}",
        "number": branch_number,
        "address1": "456 Branch Ave",
        "address2": "Unit 200",
        "city": "Branch City",
        "postal_code": "54321",
        "province": "Test Province",
        "country": "Test Country",
        "lob_id": lob_id,
        "business_id": business_id,
        "branch_manager_id": user_c_id,
        "division_name": "Test Division",
        "is_active": True
    }
    response = client.post("/api/v1/branches/", json=branch_data, headers=headers_c)
    assert response.status_code == 201, f"Failed to create branch: {response.json()}"
    branch = response.json()
    branch_id = branch["id"]

    # Step 8: Create department
    department_data = {
        "name": "HR Department",
        "description": "Human Resources Department",
        "branch_id": branch_id,
        "manager_id": None,  # We can leave it as None for now
        "is_active": True
    }
    response = client.post("/api/v1/departments/", json=department_data, headers=headers_c)
    assert response.status_code == 201, f"Failed to create department: {response.json()}"
    department = response.json()
    department_id = department["id"]

    # Verify: Get the business
    response = client.get(f"/api/v1/businesses/{business_id}", headers=headers_a)
    assert response.status_code == 200, f"Failed to get business: {response.json()}"
    assert response.json()["id"] == business_id

    # Verify: Get the branch
    response = client.get(f"/api/v1/branches/{branch_id}", headers=headers_c)
    assert response.status_code == 200, f"Failed to get branch: {response.json()}"
    assert response.json()["id"] == branch_id
    assert response.json()["business_id"] == business_id
    assert response.json()["branch_manager_id"] == user_c_id

    # Verify: Get the department
    response = client.get(f"/api/v1/departments/{department_id}", headers=headers_c)
    assert response.status_code == 200, f"Failed to get department: {response.json()}"
    assert response.json()["id"] == department_id
    assert response.json()["branch_id"] == branch_id

    # Clean up: delete in reverse order (department, branch, business)
    # Delete department
    response = client.delete(f"/api/v1/departments/{department_id}", headers=headers_c)
    assert response.status_code == 200, f"Failed to delete department: {response.json()}"

    # Delete branch
    response = client.delete(f"/api/v1/branches/{branch_id}", headers=headers_c)
    assert response.status_code == 200, f"Failed to delete branch: {response.json()}"

    # Delete business
    response = client.delete(f"/api/v1/businesses/{business_id}", headers=headers_a)
    assert response.status_code == 200, f"Failed to delete business: {response.json()}"

    # Note: We do not delete the users because there is no DELETE endpoint for users.
    # The users have unique emails, so leaving them in the database is acceptable.

if __name__ == "__main__":
    test_business_branch_department_workflow()
    print("All tests passed!")

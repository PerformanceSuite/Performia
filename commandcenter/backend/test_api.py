#!/usr/bin/env python3
"""
Simple API test script to verify endpoints work
"""

import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app


async def test_api():
    """Test basic API endpoints"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        print("Testing Command Center API...")
        print()

        # Test health endpoint
        print("1. GET /health")
        response = await client.get("/health")
        assert response.status_code == 200
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()

        # Test root endpoint
        print("2. GET /")
        response = await client.get("/")
        assert response.status_code == 200
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()

        # Test list repositories (empty)
        print("3. GET /api/v1/repositories/")
        response = await client.get("/api/v1/repositories/")
        assert response.status_code == 200
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Repositories: {len(response.json())} items")
        print()

        # Test create repository
        print("4. POST /api/v1/repositories/")
        repo_data = {
            "owner": "test-org",
            "name": "test-repo",
            "description": "Test repository"
        }
        response = await client.post("/api/v1/repositories/", json=repo_data)
        assert response.status_code == 201
        repo = response.json()
        repo_id = repo["id"]
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Created repository ID: {repo_id}")
        print()

        # Test get repository
        print(f"5. GET /api/v1/repositories/{repo_id}")
        response = await client.get(f"/api/v1/repositories/{repo_id}")
        assert response.status_code == 200
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Repository: {response.json()['full_name']}")
        print()

        # Test list technologies (empty)
        print("6. GET /api/v1/technologies/")
        response = await client.get("/api/v1/technologies/")
        assert response.status_code == 200
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Technologies: {response.json()['total']} items")
        print()

        # Test create technology
        print("7. POST /api/v1/technologies/")
        tech_data = {
            "title": "Test Technology",
            "domain": "audio-dsp",
            "status": "discovery",
            "description": "A test technology for validation"
        }
        response = await client.post("/api/v1/technologies/", json=tech_data)
        assert response.status_code == 201
        tech = response.json()
        tech_id = tech["id"]
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Created technology ID: {tech_id}")
        print()

        # Test dashboard stats
        print("8. GET /api/v1/dashboard/stats")
        response = await client.get("/api/v1/dashboard/stats")
        assert response.status_code == 200
        stats = response.json()
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Repositories: {stats['repositories']['total']}")
        print(f"   Technologies: {stats['technologies']['total']}")
        print()

        # Test delete repository
        print(f"9. DELETE /api/v1/repositories/{repo_id}")
        response = await client.delete(f"/api/v1/repositories/{repo_id}")
        assert response.status_code == 204
        print(f"   ✓ Status: {response.status_code}")
        print()

        # Test delete technology
        print(f"10. DELETE /api/v1/technologies/{tech_id}")
        response = await client.delete(f"/api/v1/technologies/{tech_id}")
        assert response.status_code == 204
        print(f"   ✓ Status: {response.status_code}")
        print()

        print("=" * 50)
        print("✅ All API tests passed!")
        print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_api())

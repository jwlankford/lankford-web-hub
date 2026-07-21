import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Test Professional Book Signup
prof_headers = {"Host": "professional.localhost"}
book_data = {
    "email": "innovator@cincy.ai",
    "first_name": "Developer-Peer",
    "tenant": ""  # Middleware overwrites this field entirely
}

response_book = requests.post(
    f"{BASE_URL}/api/v1/book/signup", 
    headers=prof_headers, 
    json=book_data
)
print(f"Book Signup Status: {response_book.status_code}")
print(f"Book Response Body: {response_book.json()}\n")


# 2. Test Academic Paper Submission
acad_headers = {"Host": "academic.localhost"}
paper_data = {
    "title": "LLM Governance Models in High-Stakes Environments",
    "authors": "Lankford, J.; Smith, A.",
    "publication_year": 2026,
    "methodology": "Quantitative Analysis",
    "tenant": ""
}

response_paper = requests.post(
    f"{BASE_URL}/api/v1/research/papers", 
    headers=acad_headers, 
    json=paper_data
)
print(f"Paper Insert Status: {response_paper.status_code}")
print(f"Paper Response Body: {response_paper.json()}\n")


# 3. Cross-Tenant Verification: Try to grab papers using the professional domain
response_leak = requests.get(
    f"{BASE_URL}/api/v1/research/papers", 
    headers=prof_headers
)
print(f"Cross-Tenant Leak Check Status: {response_leak.status_code}")
print(f"Cross-Tenant Response Body: {response_leak.json()}")
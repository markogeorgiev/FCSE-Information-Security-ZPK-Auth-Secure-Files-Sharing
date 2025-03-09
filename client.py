import requests
import secrets

SERVER_URL = "http://127.0.0.1:5000"
P = 2**256 - 189  # Same as backend
G = 5  # Generator

def register(username):
    response = requests.post(f"{SERVER_URL}/register", json={"username": username})
    data = response.json()
    if "private_key" in data:
        print("[✔] Registration successful")
        return data["private_key"]
    print("[✖] Registration failed:", data)
    return None

def login(username, private_key):
    # Step 1: Request challenge from server
    response = requests.post(f"{SERVER_URL}/login", json={"username": username})
    data = response.json()
    if "challenge" not in data:
        print("[✖] Login failed:", data)
        return False

    challenge = data["challenge"]

    # Step 2: Generate commitment
    k = secrets.randbelow(P - 1)  # Random ephemeral key
    commitment = pow(G, k, P)  # Commitment = G^k mod P

    # Step 3: Compute response
    response_value = (k + (challenge * private_key)) % (P - 1)

    # Step 4: Send response to verify
    verify_response = requests.post(f"{SERVER_URL}/verify", json={
        "username": username,
        "commitment": commitment,
        "response": response_value
    })
    verify_data = verify_response.json()

    if "message" in verify_data:
        print("[✔] Login successful")
        return True
    else:
        print("[✖] Authentication failed:", verify_data)
        return False

if __name__ == "__main__":
    username = "alice8"
    print("\n=== Registering User ===")
    private_key = register(username)

    if private_key:
        print("\n=== Logging In ===")
        login(username, private_key)

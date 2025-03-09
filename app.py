from flask import Flask, request, jsonify, session
import mysql.connector
import secrets

app = Flask(__name__)
app.secret_key = "supersecret"

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "marko123",
    "database": "zkp_auth"
}

""" Schnorr parameters """
P = 2 ** 256 - 189  # Large prime number
G = 5  # Generator

ongoing_challenges = {}


def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    private_key = secrets.randbelow(P - 1)  # Secret key
    public_key = pow(G, private_key, P)  # Public key

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, public_key) VALUES (%s, %s)", (username, public_key))
        conn.commit()
        return jsonify({"message": "User registered", "private_key": private_key})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT public_key FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        public_key = int(user["public_key"])

        # Generate challenge (random c)
        challenge = secrets.randbelow(P - 1)

        # Store challenge for user
        ongoing_challenges[username] = (public_key, challenge)

        return jsonify({"challenge": challenge})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    username = data.get("username")
    commitment = int(data.get("commitment"))
    response = int(data.get("response"))

    if username not in ongoing_challenges:
        return jsonify({"error": "No challenge found"}), 400

    public_key, challenge = ongoing_challenges.pop(username)

    # Compute verification
    lhs = pow(G, response, P)
    rhs = (commitment * pow(public_key, challenge, P)) % P

    print(f"DEBUG: LHS = {lhs}, RHS = {rhs}")  # Debugging output

    if lhs == rhs:
        session["username"] = username
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Authentication failed"}), 401


if __name__ == '__main__':
    app.run(debug=True)
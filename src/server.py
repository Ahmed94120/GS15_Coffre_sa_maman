import os
from encryption.cobra import *
from encryption.rsa import *
from encryption.hmac import *
from authentification.google_auth import *


SERVER_DIR = "./server"
USERS_DIR = os.path.join(SERVER_DIR, "Users")
REPERTOIRE_DIR = os.path.join(SERVER_DIR, "Repertoire")
LOG_FILE = os.path.join(SERVER_DIR, "journalisation.log")

def initialize_server():
    """Initialize server directories."""
    os.makedirs(USERS_DIR, exist_ok=True)
    os.makedirs(REPERTOIRE_DIR, exist_ok=True)
    open(LOG_FILE, "a").close()
    log_action("Server directories initialized successfully.")

def log_action(action):
    """Log an action to the server log file."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{get_current_time()}] {action}\n")

def get_current_time():
    """Return the current formatted time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def check_user_exists(username):
    """Check if a user already exists."""
    user_file = os.path.join(USERS_DIR, f"{username}.txt")
    exists = os.path.exists(user_file)
    log_action(f"Checked existence of user {username}: {'Exists' if exists else 'Does not exist'}.")
    return exists

def handle_user_enrollment(username, public_key):
    """
    Handle user enrollment:
    - Store the public key.
    - Create a directory for the user's files.
    - Log the action.

    Args:
        username (str): Username.
        public_key (tuple): User's public key (e, n).
    """
    user_file = os.path.join(USERS_DIR, f"{username}.txt")
    with open(user_file, "w") as file:
        file.write(f"{public_key[0]},\n{public_key[1]}")
    
    user_dir = os.path.join(REPERTOIRE_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    log_action(f"User {username} successfully enrolled with public key.")

    secret = generate_google_authenticator_secret()
    
    # Generate a QR code for Google Authenticator
    generate_google_authenticator_qr(username, secret)
    # Save the secret securely (e.g., encrypt with public key)
    save_google_authenticator_secret(username, secret)


def save_google_authenticator_secret(username, secret):
    """
    Save the Google Authenticator secret securely for a given user.
    """

    # Save the encrypted secret to a file

    secret_file_path = os.path.join(USERS_DIR, f"{username}_ga_secret.txt")
    with open(secret_file_path, "w") as f:
        f.write(secret)

def load_google_authenticator_secret(username):
    """
    Loads the Google Authenticator secret for the specified user.
    The secret is stored in an encrypted file and is decrypted using the RSA private key.

    Args:
        username (str): The username for whom the secret is being retrieved.
        private_key (tuple): The RSA private key (d, n).

    Returns:
        str: The decrypted Google Authenticator secret, or None if the secret file is missing or decryption fails.
    """
    
    secret_file = os.path.join(USERS_DIR, f"{username}_ga_secret.txt")

    if not os.path.exists(secret_file):
        print(f"[ERROR] Encrypted Google Authenticator secret not found for user: {username}.")
        return None

    try:
        # Read the encrypted secret from the file
        with open(secret_file, "r") as f:
            secret = f.read()

        # Decode the bytes back into a string
        return secret

    except Exception as e:
        print(f"[ERROR] Failed to load or decrypt Google Authenticator secret for {username}: {e}")
        return None

def load_public_key(username):
    """Load the public key from the user's directory."""
    filepath = os.path.join(SERVER_DIR, "Users", f"{username}.txt")  # Build the complete path
    try:
        with open(filepath, "r") as f:
            n, e = map(int, f.read().strip().split(","))  # Read n and e as integers
        log_action(f"Public key successfully loaded for user {username}.")
        return (n, e)
    except FileNotFoundError:
        log_action(f"Error: Public key file not found for user {username}.")
        return None
    except ValueError:
        log_action(f"Error: Invalid public key format for user {username}.")
        return None

def handle_file_upload_server(username, file_name, encrypted_data, shared_key, hmac_value):
    """
    Allow a user to upload a file to their server directory.

    Args:
        username (str): Username.
        file_name (str): File name.
        encrypted_data (bytes): Encrypted data to be stored.
        shared_key (str): Shared key for COBRA encryption.
    """
    # Decrypt the data with COBRA
    log_action(f"Starting COBRA decryption for file '{file_name}' by user {username}.")
    decrypted_data = cobra_decode(encrypted_data, shared_key)
    log_action(f"COBRA decryption completed for file '{file_name}'.")

    # Load the user's RSA public key
    public_key = load_public_key(username)
    if public_key is None:
        log_action(f"Error: Public key not found for user {username}.")
        raise ValueError(f"Public key not found for user {username}.")

    # Verify HMAC
    if not hmac_verify(decrypted_data, shared_key, hmac_value):
        log_action(f"Error: HMAC verification failed for file '{file_name}' uploaded by user {username}.")
        raise ValueError("Error: HMAC verification failed.")
    else:
        log_action(f"HMAC verification succeeded for file '{file_name}' uploaded by user {username}.")

        # Encrypt the data with RSA
        rsa_encrypted_data = rsa_encrypt(decrypted_data, public_key)
        log_action(f"Data successfully encrypted with RSA for file '{file_name}'.")

        # Save the RSA-encrypted data in the user's directory
        user_dir = os.path.join(REPERTOIRE_DIR, username)
        if not os.path.exists(user_dir):
            raise FileNotFoundError(f"User directory for {username} not found.")

        file_path = os.path.join(user_dir, file_name)
        with open(file_path, "wb") as file:
            file.write(rsa_encrypted_data)
        log_action(f"File '{file_name}' successfully stored for user {username}.")

def handle_file_download_server(username, file_name, shared_key):
    """
    Allow a user to retrieve a file stored on the server.

    Args:
        username (str): Username.
        file_name (str): File name.

    Returns:
        bytes: Encrypted file data.
    """
    user_dir = os.path.join(REPERTOIRE_DIR, username)
    file_path = os.path.join(user_dir, file_name)

    if not os.path.exists(file_path):
        log_action(f"Error: File '{file_name}' not found for user {username}.")
        raise FileNotFoundError(f"File '{file_name}' not found for user {username}.")

    with open(file_path, "rb") as file:
        data = file.read()
    log_action(f"File '{file_name}' retrieved successfully for user {username}.")

    # Generate HMAC for the file
    hmac_value = generate_hmac(data, shared_key)
    log_action(f"HMAC generated for file '{file_name}' for user {username}.")

    # Encrypt with COBRA (shared key)
    cobra_encrypted_data = cobra_encode(data, shared_key)
    log_action(f"File '{file_name}' encrypted with COBRA for user {username}.")

    return file_name, cobra_encrypted_data, hmac_value

def list_user_files(username):
    """
    List available files in the user's server directory.

    Args:
        username (str): Username.

    Returns:
        list: List of file names in the user's directory.
    """
    user_dir = os.path.join(REPERTOIRE_DIR, username)
    if not os.path.exists(user_dir):
        log_action(f"Error: Directory not found for user {username}.")
        raise FileNotFoundError(f"Directory not found for user {username}.")

    files = os.listdir(user_dir)
    log_action(f"User {username} accessed the file list: {', '.join(files)}.")
    return files
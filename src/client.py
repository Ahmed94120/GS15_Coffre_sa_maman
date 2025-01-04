from server import *
from encryption.cobra import cobra_encode, cobra_decode
import os
from encryption.hmac import *
from authentification.google_auth import *
CLIENT_DIR = "./client"

def initialize_client(username, public_key, private_key):
    """
    Initializes the client directory and saves the generated public and private keys.

    Args:
        username (str): The username.
        public_key (tuple): The user's public key (n, e).
        private_key (tuple): The user's private key (n, d).
    """
    # Create a user-specific directory
    client_user_dir = os.path.join(CLIENT_DIR, username)
    os.makedirs(client_user_dir, exist_ok=True)

    # Save the private key
    private_key_file = os.path.join(client_user_dir, "private_key.txt")
    with open(private_key_file, "w") as file:
        file.write(f"{private_key[0]},\n{private_key[1]}")

    # Save the public key
    public_key_file = os.path.join(client_user_dir, "public_key.txt")
    with open(public_key_file, "w") as file:
        file.write(f"{public_key[0]},\n{public_key[1]}")

    print(f"Client directory initialized for {username}. Keys have been generated and saved.")

def load_private_key(username):
    """
    Loads the private key for the user.

    Args:
        username (str): The username.

    Returns:
        tuple: The private key (n, d) or None if not found or invalid.
    """
    filepath = os.path.join(CLIENT_DIR, username, "private_key.txt")
    try:
        with open(filepath, "r") as f:
            n, d = map(int, f.read().strip().split(","))  # Parse n and d as integers
        return (n, d)
    except FileNotFoundError:
        print(f"Error: Private key file not found at {filepath}.")
        return None
    except ValueError:
        print("Error: Invalid private key format.")
        return None

def upload_file_client_to_serv(username, shared_key, file_path):
    """
    Handles the process of uploading a file by encrypting it with COBRA and RSA.

    Args:
        username (str): The username.
        shared_key (str): The shared key from Diffie-Hellman.
        file_path (str): Path to the file to upload.

    Returns:
        tuple: The encrypted file name, COBRA-encrypted data, and HMAC value.
    """
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    # Read the file content
    with open(file_path, "rb") as file:
        data = file.read()

    # Generate the HMAC for the file
    hmac_value = generate_hmac(data, shared_key)

    # Encrypt the data with COBRA
    cobra_encrypted_data = cobra_encode(data, shared_key)

    # Prepare the encrypted file name
    encrypted_file_name = os.path.basename(file_path) + ".enc"

    return encrypted_file_name, cobra_encrypted_data, hmac_value

def download_file(username, shared_key, encrypted_file_name_by_cobra, cobra_encrypted_data, hmac_value):
    """
    Handles the process of downloading a file by decrypting it with RSA and COBRA.

    Args:
        username (str): The username.
        shared_key (str): The shared key from Diffie-Hellman.
        encrypted_file_name_by_cobra (str): The name of the encrypted file.
        cobra_encrypted_data (bytes): COBRA-encrypted data.
        hmac_value (str): The HMAC value to verify data integrity.

    Raises:
        ValueError: If HMAC verification fails.
    """
    # Load the user's private key
    private_key = load_private_key(username)
    if private_key is None:
        raise ValueError(f"Private key for user {username} not found.")

    # Decrypt the data with COBRA
    rsa_encrypt_data = cobra_decode(cobra_encrypted_data, shared_key)

    # Verify the HMAC
    if not hmac_verify(rsa_encrypt_data, shared_key, hmac_value):
        log_action(f"Error: HMAC mismatch for file '{encrypted_file_name_by_cobra}' uploaded by user {username}.")
        raise ValueError("Error: HMAC verification failed.")
    else:
        log_action(f"HMAC verification succeeded for file '{encrypted_file_name_by_cobra}' uploaded by user {username}.")

    # Decrypt the data with RSA
    rsa_decrypted_data = rsa_decrypt(rsa_encrypt_data, private_key)

    # Save the decrypted file to the client's directory
    client_user_dir = os.path.join(CLIENT_DIR, username, "Repertoire")
    os.makedirs(client_user_dir, exist_ok=True)

    # Determine the original file name
    decrypted_file_name = encrypted_file_name_by_cobra.replace(".enc", "")
    output_file_path = os.path.join(client_user_dir, decrypted_file_name)

    with open(output_file_path, "wb") as file:
        file.write(rsa_decrypted_data)

    print(f"File '{decrypted_file_name}' successfully downloaded and decrypted.")


def handle_user_authentication(username):
    """
    Authenticates the user using Google Authenticator.
    """
    # Load the secret securely (e.g., decrypt with private key)
    secret = load_google_authenticator_secret(username)

    # Prompt for the TOTP code
    user_code = input("Enter your Google Authenticator code: ")

    if verify_google_authenticator_code(secret, user_code):
        print("Authentication successful.")
        return True
    else:
        print("Authentication failed. Invalid code.")
        return False
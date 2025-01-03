from encryption.diffiehellman import parametres_globaux, private_key, mod_exp, diffiehellman
from server import *
from client import *
from encryption.rsa import rsa_key_derivaded
from authentification.zkp import ZeroKnowledgeProof

def handle_diffie_hellman():
    """
    Handles the Diffie-Hellman key exchange between the client and server.
    Ensures the shared key is securely derived and consistent on both sides.
    """
    print("\n=== Diffie-Hellman Key Exchange ===")
    
    # Generate global parameters for Diffie-Hellman
    p, g = parametres_globaux()
    
    # Server generates its private and public keys
    private_key_server = private_key(p)
    public_key_server = mod_exp(g, private_key_server, p)
    print(f"Server Public Key: {public_key_server}")

    # Client generates its private and public keys
    private_key_client = private_key(p)
    public_key_client = mod_exp(g, private_key_client, p)
    print(f"Client Public Key: {public_key_client}")

    # Compute shared keys on both sides
    shared_key_server = str(diffiehellman(public_key_client, private_key_server, p))
    shared_key_client = str(diffiehellman(public_key_server, private_key_client, p))

    # Ensure shared keys match
    print()
    assert shared_key_server == shared_key_client, "Error: Shared keys do not match!"
    print(f"Shared key successfully generated: {shared_key_client}")
    return shared_key_client

def handle_file_operations(username, shared_key):
    """
    Manages file operations, including upload, download, and listing files.
    """
    while True:
        print("\n=== File Management ===")
        print("1. Upload a file")
        print("2. List available files")
        print("3. Download a file")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            # Upload file
            file_path = input("Enter the path of the file to upload: ")
            encrypted_file_name, cobra_encrypted_data, hmac_value = upload_file_client_to_serv(username, shared_key, file_path)
            handle_file_upload_server(username, encrypted_file_name, cobra_encrypted_data, shared_key, hmac_value)

        elif choice == "2":
            # List files available on the server
            files = list_user_files(username)
            print("\nFiles available in your server directory:")
            for file in files:
                print(f"- {file}")

        elif choice == "3":
            # Download a specific file
            file_name = input("Enter the name of the file to download: ")
            encrypted_file_name, cobra_encrypted_data, hmac_value = handle_file_download_server(username, file_name, shared_key)
            download_file(username, shared_key, encrypted_file_name, cobra_encrypted_data, hmac_value)

        elif choice == "4":
            # Exit to main menu
            print("Returning to the main menu.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    initialize_server()
    print("\nWelcome to the secure vault system.")
    
    choice = input("\n=== Would you like to create an account (1) or authenticate (2)? (1/2): === ")

    if choice == "1":
        # User enrollment
        username = input("Enter the username for enrollment: ")
        if check_user_exists(username):
            print(f"Error: User {username} already exists.")
        else:
            password = input("Enter a password: ")
            public_key, private_key = rsa_key_derivaded(password)
            
            # Initialize client directory and save keys
            initialize_client(username, public_key, private_key)
            
            # Save user information on the server
            handle_user_enrollment(username, public_key)
            print(f"User {username} successfully enrolled.")

    elif choice == "2":
        # User authentication
        username = input("Enter your username: ")
        if not check_user_exists(username):
            print(f"Error: User {username} does not exist. Please create an account.")
        else:
            print(f"Authenticating user {username}...")
            
            # Perform Zero Knowledge Proof for authentication
            connected = ZeroKnowledgeProof(load_public_key(username), load_private_key(username))
            if connected:
                print(f"Authentication successful for user {username}.")
                shared_key = handle_diffie_hellman()
                handle_file_operations(username, shared_key)
            else:
                print("Authentication failed. Access denied.")

    print("Thank you for using the secure vault system. Program terminated.")
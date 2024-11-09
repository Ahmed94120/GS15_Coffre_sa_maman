from key_management.user_enrollment import enroll_user

if __name__ == "__main__":
    username = input("Entrez le nom d'utilisateur pour l'enrôlement : ")
    enroll_user(username)
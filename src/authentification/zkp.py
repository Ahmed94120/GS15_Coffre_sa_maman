import random
import os


def gcd(a, b):
    """Calculate the greatest common divisor (GCD) of two numbers."""
    while b != 0:
        a, b = b, a % b
    return a


def generate_coprime(n):
    """Generate a random number B that is coprime with n."""
    while True:
        B = random.randint(1, n - 1)
        if gcd(B, n) == 1:
            return B


class ZeroKnowledgeProof:
    def __init__(self, public_key, private_key):
        if not public_key or not private_key:
            raise ValueError("Public and private keys are required.")
        self.public_key = public_key
        self.private_key = private_key
        self.T_n = None
        self.d = None

    def prover_step(self):
        """Execute the prover logic."""
        d, n_prover, = self.private_key

        # Step 1: Generate B and retrieve e from verifier
        B = generate_coprime(n_prover)
        e = self.verifier_step(step="send_e")

        # Step 2: Compute J
        try:
            J = pow(pow(B, -1, n_prover), e, n_prover)
        except ValueError:
            raise ValueError("Failed to calculate modular inverse. Check coprimality of B and n_prover.")

        # Step 3: Generate r and compute T
        r = random.randint(1, n_prover - 1)
        T = pow(r, e, n_prover)

        # Step 4: Send T to verifier and receive d
        self.d = self.verifier_step(step="send_d", T=T, J=J, e=e)

        # Step 5: Compute t and send it to verifier
        t = (r * pow(B, self.d, n_prover)) % n_prover
        result = self.verifier_step(step="verify", t=t, J=J, e=e)

        return result == "success"

    def verifier_step(self, step, T=None, t=None, J=None, e=None):
        """Execute the verifier logic."""
        e_verifier, n_verifier, = self.public_key

        if step == "send_e":
            return e_verifier
        elif step == "send_d":
            self.T_n = T
            self.d = random.randint(0, e_verifier - 1)
            return self.d
        elif step == "verify":
            P = (pow(t, e_verifier, n_verifier) * pow(J, self.d, n_verifier)) % n_verifier
            return "success" if P == self.T_n else "failure"
        else:
            raise ValueError("Invalid step in verifier.")

    def authenticate(self):
        """Run the Zero-Knowledge Proof authentication."""
        try:
            return self.prover_step()
        except Exception as e:
            print(f"Error during ZKP: {e}")
            return False
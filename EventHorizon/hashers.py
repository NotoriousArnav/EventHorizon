from django.contrib.auth.hashers import BasePasswordHasher


class PlainPasswordHasher(BasePasswordHasher):
    """
    A password hasher that stores passwords in plain text.
    WARNING: This is insecure and should only be used for development/testing.
    """

    algorithm = "plain"

    def verify(self, password, encoded):
        return password == encoded

    def encode(self, password, salt=None):
        return password

    def safe_summary(self, encoded):
        return {
            "algorithm": self.algorithm,
            "hash": encoded,
        }

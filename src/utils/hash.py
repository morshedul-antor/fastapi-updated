from passlib.context import CryptContext
hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def create_hash(data: str) -> str:
        return hash_context.hash(data)

    @staticmethod
    def validate_hash(plain_data: str, hashed_data: str) -> bool:
        return hash_context.verify(plain_data, hashed_data)

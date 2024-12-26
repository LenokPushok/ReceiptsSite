import jwt
from api.settings import jwt_settings
from api.utils.dto import TokenData
from api.utils.exceptions import JWTToolError
from pydantic import ValidationError


class JWTTool:
    def __init__(self):
        self.algorithm = "HS256"
        self.secret_key = jwt_settings.secret_key

    def generate_token(self, **encoded_data) -> str:
        return jwt.encode(encoded_data, self.secret_key, self.algorithm)

    def decode_token(self, token: str) -> TokenData:
        try:
            decoded_data = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            return TokenData.model_validate(decoded_data)
        except jwt.PyJWTError as e:
            raise JWTToolError(detail=str(e)) from e
        except ValidationError as e:
            raise JWTToolError(detail="Cannot validate payload") from e


jwt_tool = JWTTool()

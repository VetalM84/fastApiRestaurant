"""Dependencies for auth."""

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm.session import Session
from starlette import status

from app.crud import utils
from app.db.database import get_db
from app.db.models import Waiter

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Waiter:
    """Decode token when accessing a secure endpoint and return a Waiter object whether token is valid."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token=token, key=utils.SECRET_KEY, algorithms=[utils.ALGORITHM]
        )
        username: str = payload.get("sub")
        user = utils.get_user_by_username(db, username=username)
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user


class JWTBearer(HTTPBearer):
    """Class for authentication with JWT."""

    def __init__(self, auto_error: bool = True):
        """Enable automatic error reporting."""
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """Define a variable called 'credentials' of type HTTPAuthorizationCredentials,
        which is created when the 'JWTBearer' class is invoked."""
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_token(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_token(token: str) -> bool:
        """Decode token and return True, False - if it is not valid."""
        try:
            jwt.decode(token=token, key=utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        except JWTError:
            return False
        return True

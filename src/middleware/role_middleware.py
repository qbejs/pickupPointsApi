from fastapi import HTTPException, Depends

from src.db import User
from src.models.users import current_active_user


class RoleCheck:
    role: str = None
    user: User = None

    def __init__(self, role: str):
        self.role = role

    def __call__(self, user: User = Depends(current_active_user)):
        if user.has_role(self.role):
            print(f"Access granted to user: {user.id}")
            return True

        raise HTTPException(403, 'Forbidden')


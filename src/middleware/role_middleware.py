from fastapi import HTTPException, Depends
import logging as logger
from src.db import User
from src.models.users import current_active_user


class RoleCheck:
    role: str = None
    user: User = None
    access_granted: False

    def __init__(self, role: str):
        self.role = role

    def __call__(self, user: User = Depends(current_active_user)):
        if user.has_role(self.role):
            self.access_granted = True
            logger.info({
                "user": user.get_info(),
                "requested_role": self.role,
                "role_validation": self.access_granted
            })
            return self

        raise HTTPException(403, 'Forbidden')

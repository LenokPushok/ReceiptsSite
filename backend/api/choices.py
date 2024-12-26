from enum import Enum


class Role(str, Enum):
    user = "User"
    admin = "Admin"


class ReviewStatus(str, Enum):
    approved = "approved"
    pending = "pending"
    unapproved = "unapproved"

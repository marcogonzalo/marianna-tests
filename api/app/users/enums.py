from enum import Enum


class UserRole(str, Enum):
    ASSESSMENT_DEVELOPER = "assessment_developer"
    ASSESSMENT_REVIEWER = "assessment_reviewer"
    ADMIN = "admin"

    def serialize(self):
        return self.value

all_user_roles = [role.value for role in UserRole]

class Gender(str, Enum):
    FEMALE = "female"
    MALE = "male"
    OTHER = "other"

    def serialize(self):
        return self.value

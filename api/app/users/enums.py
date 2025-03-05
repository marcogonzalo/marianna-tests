from enum import Enum


class UserRole(str, Enum):
    ASSESSMENT_DEVELOPER = "assessment_developer"
    ASSESSMENT_TAKER = "assessment_taker"
    ADMIN = "admin"

    def serialize(self):
        return self.value


class Gender(str, Enum):
    FEMALE = "female"
    MALE = "male"
    OTHER = "other"

    def serialize(self):
        return self.value

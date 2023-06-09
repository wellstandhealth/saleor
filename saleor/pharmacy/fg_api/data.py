class LanguagePreferenceData:
    @staticmethod
    def build(data):
        return LanguagePreferenceData(
            uuid=data.get('uuid'),
            code=data.get('code'),
            name=data.get('name'))

    def __init__(self, uuid, code, name):
        self.uuid = uuid
        self.code = code
        self.name = name


class PatientData:
    @staticmethod
    def build(data):
        return PatientData(
            uuid=data["uuid"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            gender_assigned_at_birth=data["gender_assigned_at_birth"],
            date_of_birth=data["date_of_birth"],
            email=data["email"],
            phone_number=data["phone_number"],
            language_preference=data["language_preference"],
        )

    def __init__(self, uuid, first_name, last_name, gender_assigned_at_birth,
                 date_of_birth, email, phone_number, language_preference):
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name
        self.gender_assigned_at_birth = gender_assigned_at_birth
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone_number = phone_number
        self.language_preference = language_preference

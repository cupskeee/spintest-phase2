from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ReferenceField,
    CASCADE
)
from flask_bcrypt import generate_password_hash, check_password_hash


class Users(Document):
    _id = StringField(required=True, primary_key=True)
    first_name = StringField(required=True, max_length=25)
    last_name = StringField(required=True, max_length=25)
    phone_number = StringField(required=True, unique=True, max_length=25)
    address = StringField(default="")
    pin = StringField(required=True)
    wallet = ReferenceField('Wallets', reverse_delete_rule=CASCADE)
    created_date = DateTimeField(default=datetime.now())

    meta = {'allow_inheritance': True}

    def generate_pw_hash(self):
        self.pin = generate_password_hash(password=self.pin).decode('utf-8')

    generate_pw_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, pin: str) -> bool:
        return check_password_hash(pw_hash=self.pin, password=pin)

    check_pw_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        if self._created:
            self.generate_pw_hash()
        super(Users, self).save(*args, **kwargs)
        return self

    def update(self, **kwargs):
        # Return self document after updating
        super(Users, self).update(**kwargs)
        return self

    def serialize(self):
        return_data = []

        if isinstance(self, Document):
            return_data.append(("id", str(self.id)))

        for field_name in self._fields:

            if field_name in ("id",):
                continue

            data = self._data[field_name]

            if isinstance(self._fields[field_name], DateTimeField):
                return_data.append((field_name, str(data.isoformat())))
            elif isinstance(self._fields[field_name], StringField):
                return_data.append((field_name, str(data)))

        return dict(return_data)

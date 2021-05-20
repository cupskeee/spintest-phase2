import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, PasswordField


class Registration(FlaskForm):
    class Meta:
        csrf = False
    first_name = StringField(u'First name', [validators.required(), validators.length(max=25)])
    last_name = StringField(u'Last name', [validators.required(), validators.length(max=25)])
    phone_number = StringField(u'Phone number', [validators.required(), validators.length(max=25)])
    address = TextAreaField(u'Address', [validators.optional()])
    pin = PasswordField(u'PIN', [validators.required(), validators.length(max=6)])

    def validate_phone(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise validators.ValidationError('Invalid phone number')


class Login(FlaskForm):
    class Meta:
        csrf = False
    phone_number = StringField(u'Phone number', [validators.required(), validators.length(max=25)])
    pin = PasswordField(u'PIN', [validators.required(), validators.length(max=6)])

    def validate_phone(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise validators.ValidationError('Invalid phone number')


class Update(FlaskForm):
    class Meta:
        csrf = False
    first_name = StringField(u'First name', [validators.optional(), validators.length(max=25)])
    last_name = StringField(u'Last name', [validators.optional(), validators.length(max=25)])
    address = TextAreaField(u'Address', [validators.optional()])

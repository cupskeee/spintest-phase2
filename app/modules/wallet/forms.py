import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators, PasswordField, DecimalField


class TopUp(FlaskForm):
    class Meta:
        csrf = False
    amount = DecimalField(u'amount', [validators.required()])

class Transfer(FlaskForm):
    class Meta:
        csrf = False
    target_user = StringField(u'target', [validators.required()])
    amount = DecimalField(u'amount', [validators.required()])
    remarks = TextAreaField(u'remarks', [validators.optional()], default="")

class Payment(FlaskForm):
    class Meta:
        csrf = False
    amount = DecimalField(u'amount', [validators.required()])
    remarks = TextAreaField(u'remarks', [validators.required()])

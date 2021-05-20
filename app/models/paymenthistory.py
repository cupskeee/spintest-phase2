from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    DecimalField,
    ReferenceField,
)


class PaymentHistory(Document):
    _id = StringField(required=True, primary_key=True)
    created_date = DateTimeField(default=datetime.now())
    amount = DecimalField(required=True, default=0, min_value=0)
    wallet = ReferenceField('Wallets')
    balance_before = DecimalField(required=True, default=0, min_value=0)
    balance_after = DecimalField(required=True, default=0, min_value=0)
    remarks = StringField(required=True)

    meta = {'allow_inheritance': True}

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
            elif isinstance(self._fields[field_name], DecimalField):
                return_data.append((field_name, float(data)))
            elif isinstance(self._fields[field_name], ReferenceField):
                return_data.append((field_name, data.serialize()))


        return dict(return_data)
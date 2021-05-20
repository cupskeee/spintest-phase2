from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ReferenceField,
    DecimalField
)


class Wallets(Document):
    _id = StringField(required=True, primary_key=True)
    balance = DecimalField(required=True, default=0, min_value=0)
    user = ReferenceField('Users')
    created_date = DateTimeField(default=datetime.now())

    meta = {'allow_inheritance': True}

    def update(self, **kwargs):
        # Return self document after updating
        super(Wallets, self).update(**kwargs)
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
            elif isinstance(self._fields[field_name], DecimalField):
                return_data.append((field_name, float(data)))

        return dict(return_data)

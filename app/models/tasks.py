import rq
import redis
from datetime import datetime
from flask import current_app
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ReferenceField,
    BooleanField
)


class Tasks(Document):
    task_id = StringField(required=True, max_length=36, primary_key=True)
    name = StringField(required=True, max_length=128)
    description = StringField(required=True, max_length=128)
    user = ReferenceField('Users', required=True)
    complete = BooleanField(default=False)
    created_date = DateTimeField(default=datetime.now())

    meta = {'allow_inheritance': True}

    def save(self, **kwargs):
        # Return self document after updating
        super(Tasks, self).save(**kwargs)
        return self

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100

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

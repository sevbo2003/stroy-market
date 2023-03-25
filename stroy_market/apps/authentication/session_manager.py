from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session


class CustomSessionStore(SessionStore):
    def load(self):
        try:
            s = Session.objects.get(session_key=self.session_key)
            return self.decode(s.session_data)
        except (Session.DoesNotExist, AttributeError):
            self.create()
            return {}

    def save(self, must_create=False):
        s = Session(
            session_key=self.session_key,
            session_data=self.encode(self._get_session(no_load=must_create)),
            expire_date=self.get_expiry_date(),
        )
        s.save()

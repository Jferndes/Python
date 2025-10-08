from POO.Exercice6.Base.CooperativeBase import CooperativeBase
from datetime  import datetime

class TimestampedMixin(CooperativeBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    
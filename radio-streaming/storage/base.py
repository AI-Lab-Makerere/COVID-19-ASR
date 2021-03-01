from sqlalchemy.ext.automap import automap_base
from sqlalchemy_mixins import SmartQueryMixin, ActiveRecordMixin, ReprMixin

Base = automap_base()


class BaseModel(Base, SmartQueryMixin, ActiveRecordMixin, ReprMixin):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__
    pass

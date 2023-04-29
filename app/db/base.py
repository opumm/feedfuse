# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.feeds import Feed  # noqa
from app.models.items import Item  # noqa
from app.models.read_status import ReadStatus  # noqa
from app.models.subscription import Subscription  # noqa
from app.models.users import User  # noqa

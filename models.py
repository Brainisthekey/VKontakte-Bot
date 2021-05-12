from pony.orm import Database, Required, Json
from setting import DB_CONFIG

db = Database()
db.bind(DB_CONFIG)


class UserState(db.Entity):

    """State user into scenario"""
    scenario_name = Required(str, unique=True)
    step_name = Required(str)
    context = Required(Json)
    user_id = Required(str)

class Registration(db.Entity):

    """Request for registration"""
    name = Required(str)
    email = Required(str)

db.generate_mapping(create_tables=True)
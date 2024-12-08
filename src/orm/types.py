from typing import Annotated, Literal

from sqlalchemy.orm import mapped_column

int_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

sex = Literal['M', 'F']

weekday = Literal['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

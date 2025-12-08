
import dataclasses

@dataclasses.dataclass
class Todo:
    id: int
    description: str
    completed: bool = False

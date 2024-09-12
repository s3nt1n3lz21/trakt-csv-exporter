from dataclasses import dataclass
from typing import Optional

@dataclass
class ShowCSV:
    title: str
    release_date: Optional[str]  # Optional, in case the release date is not available
    rating: Optional[float]  # Optional, in case the rating is not available

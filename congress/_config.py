from dataclasses import dataclass


@dataclass(frozen=True)
class CongressConfig:
    """
    General config info that gets passed around
    """

    congress: int
    apiKey: str

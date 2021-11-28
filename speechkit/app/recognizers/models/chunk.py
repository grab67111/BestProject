from dataclasses import dataclass, field


@dataclass
class Chunk:
    alternatives: list[str] = field(default_factory=list)
    is_final: bool = False

    def to_dict(self):
        return {
            'text': self.alternatives[0],
            'is_final': self.is_final
        }

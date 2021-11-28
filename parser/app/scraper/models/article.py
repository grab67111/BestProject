from dataclasses import dataclass, field


@dataclass
class Article:
    title: str
    body: str
    images: list[str] = field(default_factory=list)
    videos: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def __str__(self):
        return self.title

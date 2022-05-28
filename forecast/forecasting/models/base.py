from typing import Protocol

class Model(Protocol):

    def predict(self) -> int:
        pass

    def fit(self) -> None:
        pass
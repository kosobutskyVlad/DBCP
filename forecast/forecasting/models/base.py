from abc import ABC, abstractmethod

class Model(ABC):
    
    @abstractmethod
    def predict(self):
        pass
    
    @abstractmethod
    def fit(self):
        pass
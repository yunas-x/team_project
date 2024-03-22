from abc import ABC, abstractmethod
from enums import PlanType


class BaseLoader(ABC):
    @abstractmethod
    def load(self, path: str):
        """Load study plans to a folder with specified path

        Args:
            path (str): Path to folder, where downloaded files will be stored
        """
        raise NotImplemented
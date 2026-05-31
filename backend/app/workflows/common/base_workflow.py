from abc import ABC, abstractmethod

class BaseWorkflow(ABC):

    @abstractmethod
    async def execute(self, state):
        pass
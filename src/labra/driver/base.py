# src/labra/drivers/base.py
from abc import ABC, abstractmethod

class BaseDriver(ABC):
    """
    Abstract base class for all test drivers.
    Provides a uniform interface for setup, execution, and teardown.
    """

    def __init__(self, config):
        """
        Initialize the driver with a given config dictionary.

        Args:
            config (dict): Driver-specific configuration settings.
        """
        self.config = config

    @abstractmethod
    def setup(self):
        """
        Optional setup routine before executing tests (e.g., environment prep).
        """
        pass

    @abstractmethod
    def execute(self, command_or_payload):
        """
        Execute a test action against the target system.

        Args:
            command_or_payload (Any): The command or payload for execution.

        Returns:
            Any: Output or response to be used in assertions or logging.
        """
        pass

    @abstractmethod
    def teardown(self):
        """
        Optional cleanup routine after tests have finished.
        """
        pass
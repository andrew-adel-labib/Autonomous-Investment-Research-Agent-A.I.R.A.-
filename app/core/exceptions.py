class AIRAException(Exception):
    """Base application exception."""
    pass

class DataSourceError(AIRAException):
    """Raised when external data retrieval fails."""
    pass

class AgentExecutionError(AIRAException):
    """Raised when an agent step fails."""
    pass

class JobNotFoundError(AIRAException):
    """Raised when a job does not exist."""
    pass
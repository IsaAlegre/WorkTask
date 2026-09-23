class DomainError(Exception):
    """Base de todos los errores de negocio."""


class ValidationError(DomainError):
    pass


class NotFoundError(DomainError):
    pass


class InvalidTransitionError(DomainError):
    pass


class BusinessRuleError(DomainError):
    pass
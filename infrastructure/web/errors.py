from flask import Flask, jsonify

from domain.exceptions import (
    BusinessRuleError, DomainError, InvalidTransitionError, NotFoundError, ValidationError,
)

HTTP_STATUS_BY_ERROR = {
    NotFoundError: 404,
    ValidationError: 422,
    InvalidTransitionError: 409,
    BusinessRuleError: 409,
}


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(DomainError)
    def handle_domain_error(error: DomainError):
        status = HTTP_STATUS_BY_ERROR.get(type(error), 400)
        return jsonify({"error": str(error)}), status
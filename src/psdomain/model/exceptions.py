class PROMOException(Exception):
    pass


class BadRequest(PROMOException):
    pass


class InvalidProductId(BadRequest):
    pass


class InvalidFobId(BadRequest):
    pass


class InvalidSupplier(BadRequest):
    pass


class NotFoundException(PROMOException):
    pass


class InvalidSupplierCode(NotFoundException):
    def __init__(self, supplier_code: str):
        self.supplier_code = supplier_code

    def __str__(self):
        return f"Supplier with code {self.supplier_code} is not available."


class InvalidServiceVersion(NotFoundException):
    def __init__(self, supplier_code: str, service_code: str, version: str, environment: str):
        self.supplier_code = supplier_code
        self.service_code = service_code
        self.version = version
        self.environment = environment or 'PROD'

    def __str__(self):
        return (f"{self.supplier_code}: Service with code {self.service_code}:{self.version} for {self.environment} "
                f"is not available.")


class UnhandledException(BadRequest):
    pass

class UnsupportedFileTypeError(Exception):
    """Raised when a file type is not supported for a given customer."""
    pass


class WorkbookValidationError(Exception):
    """Raised when the workbook cannot be opened or validated."""
    pass


class MissingRequiredHeaderError(WorkbookValidationError):
    """Raised when one or more required headers are missing."""
    pass
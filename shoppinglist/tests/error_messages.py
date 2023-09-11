from rest_framework.exceptions import ErrorDetail


class ERRORS:
    INCORRECT_TYPE_ERROR = ErrorDetail(
        string="Incorrect type. Expected pk value, received str.", code="incorrect_type"
    )
    INVALID_BOOLEAN_ERROR = ErrorDetail(
        string="Must be a valid boolean.", code="invalid"
    )
    INVALID_CHOICE_ERROR_UNIT = ErrorDetail(
        string='"invalid_unit" is not a valid choice.', code="invalid_choice"
    )
    INVALID_CHOICE_ERROR_CATEGORY = ErrorDetail(
        string='"123" is not a valid choice.', code="invalid_choice"
    )
    MIN_QUANTITY_ERROR = "Ensure this value is greater than or equal to 1."
    FIELD_REQUIRED_ERROR = ["This field is required."]
    NOT_FOUND_ERROR = {"detail": "Not found."}
    SH_LIST_NOT_FOUND_ERROR = {
        "detail": ErrorDetail(string="ShoppingList not found.", code="not_found")
    }

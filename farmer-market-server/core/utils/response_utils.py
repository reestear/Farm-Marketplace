from rest_framework.response import Response


def create_response_schema(data_schema, status="success"):
    """
    Generates a response schema with the provided data schema.

    Args:
        data_schema (dict): The schema for the `data` field.
        status (str): The status value, either "success" or "error".

    Returns:
        dict: The complete response schema.
    """
    if status not in ["success", "error"]:
        raise ValueError("Status must be either 'success' or 'error'.")

    return {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": [status],
                "example": status,
            },
            "data": data_schema,
        },
        "required": ["status", "data"],
    }


base_success_response_schema = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["success"],
            "example": "success",
        },
        "data": {
            "type": "object",
            "additionalProperties": True,
        },
    },
    "required": ["status", "data"],
}

base_error_response_schema = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["error"],
            "example": "error",
        },
        "data": {
            "type": "object",
            "additionalProperties": True,
        },
    },
    "required": ["status", "data"],
}


class SuccessResponse(Response):
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):

        super().__init__(
            {
                "status": "success",
                "data": data,
            },
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )


class ErrorResponse(Response):
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):

        super().__init__(
            {
                "status": "error",
                "data": data,
            },
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )

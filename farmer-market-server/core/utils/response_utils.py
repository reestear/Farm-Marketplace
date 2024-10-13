from rest_framework.response import Response


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

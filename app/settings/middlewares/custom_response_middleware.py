from fastapi import Request, Response, HTTPException


async def custom_response_middleware(request: Request, call_next):
    response = await call_next(request)

    print(response)
    print(response.status_code)
    # print(response.detail)
    if response.status_code >= 400:
        if isinstance(response, HTTPException):
            # Handle HTTPException separately
            custom_response = {
                "status": "error",
                "error_message": response.detail
            }
        else:
            # Format other error responses
            custom_response = {
                "status": "error",
                "error_message": response.body.decode()  # Assuming error message is in the response body
            }
    else:
        custom_response = {
            "status": "success",
            "data": response.body
        }

    response.body = custom_response
    return response

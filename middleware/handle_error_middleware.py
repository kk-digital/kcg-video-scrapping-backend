from fastapi import HTTPException, Request


class KcgRequestsMiddleware:
    """
    Includes a function called "process_requests" that works as a FastAPI middleware. The function does some
    important things:

        - Processes all the uncatched errors raised during the excecution of any endpoint and returns a standarized
        error response to the client, instead of a plain error 500 responses that FastAPI would return by default.

        - Makes the request object include an object for creating standarized API responses. The object can be accesed
        in the endpoints code in "request.state.response_handler".
    """

    @staticmethod
    async def process_requests(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            print("Failed to process requests", e)
            raise e
        except Exception as e:
            print("Failed to process requests", e)
            raise HTTPException(status_code=500, detail="Internal Server Error")

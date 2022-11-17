import threading


class RequestResponseMiddleware:
    def __init__(self, get_response, thread_local=threading.local()):
        self.get_response = get_response
        self.thread_local = thread_local
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.thread_local.current_request = request
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

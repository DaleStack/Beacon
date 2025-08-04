from django.http import HttpResponse
import re

MOBILE_USER_AGENT_REGEX = re.compile(
    r".*(iphone|mobile|android|blackberry|nokia|phone|opera mini|windows phone)", re.IGNORECASE
)

class BlockMobileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        if MOBILE_USER_AGENT_REGEX.match(user_agent):
            return HttpResponse(
                "<h2>Sorry, this web application is only available on desktop devices.</h2>",
                content_type="text/html",
                status=403
            )
        return self.get_response(request)

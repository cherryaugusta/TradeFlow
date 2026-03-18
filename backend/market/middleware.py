import logging
import time

logger = logging.getLogger(__name__)


class RequestLatencyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.perf_counter()
        response = self.get_response(request)
        elapsed_ms = (time.perf_counter() - started_at) * 1000

        logger.info(
            "Request Latency | method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.path,
            getattr(response, "status_code", "unknown"),
            elapsed_ms,
        )
        return response

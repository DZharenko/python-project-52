from rollbar.contrib.django.middleware import RollbarNotifierMiddleware


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):

    def get_extra_data(self, request, exc):
        return {
            "trace_id": "aabbccddeeff",
            "feature_flags": ["feature_1", "feature_2"],
        }

    def get_payload_data(self, request, exc):
        if not request.user.is_anonymous:
            return {
                "person": {
                    "id": request.user.id,
                    "username": request.user.username,
                }
            }
        return {}
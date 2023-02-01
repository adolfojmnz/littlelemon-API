from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class UserTenCallsPerMinute(UserRateThrottle):
    scope = 'ten-per-minute'


class UserTenCallsPerHour(UserRateThrottle):
    scope = 'ten-per-hour'


class AnonTenCallsPerHour(AnonRateThrottle):
    scope = 'ten-per-hour'


class AnonZeroCalls(AnonRateThrottle):
    scope = 'zero'


class UserThrottleMixin:
    throttle_classes = []
    action = None

    def get_throttles(self):
        if self.action == 'list':
            throttle_classes = [UserTenCallsPerMinute]
        else:
            throttle_classes = [UserTenCallsPerHour]
        return [throttle() for throttle in throttle_classes]


class AnonThrottleMixin(AnonRateThrottle):
    throttle_classes = []
    action = None

    def get_throttles(self):
        if self.action == 'list':
            throttle_classes = [AnonTenCallsPerHour]
        else:
            throttle_classes = [AnonZeroCalls]
        return [throttle() for throttle in throttle_classes]
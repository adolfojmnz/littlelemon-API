from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class TenCallPerMinute(UserRateThrottle):
    scope = 'ten-minute'


class TenCallPerHour(AnonRateThrottle):
    scope = 'ten-hour'

class DistanceRangeNotFoundError(Exception):
    pass
class DistanceTooLargeError(Exception):
    pass
class VenueDataServiceError(Exception):
    def __init__(self, message: str):
        self.message = message
    pass
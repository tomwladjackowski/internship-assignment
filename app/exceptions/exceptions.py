class DistanceRangeNotFoundError(Exception):
    # Raised when no distance range is found.
    pass
class DistanceTooLargeError(Exception):
    # Raised when distance between user and venue is outside of the possible delivery range
    pass
class VenueDataServiceError(Exception):
    pass
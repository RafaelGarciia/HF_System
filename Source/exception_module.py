# Used when you hear an error when loading the Json configuration file.
class LoadConfigError(Exception):
    def __init__(self, message):            
        # Call the base class constructor with the parameters it needs.
        super().__init__(message)
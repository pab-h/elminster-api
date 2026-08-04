class UserNotFoundException(Exception):
    pass

class UserEmailAlredyExistsException(Exception):
    pass

class BoardNotFoundException(Exception):
    pass

class WallpaperIsTooLargeException(Exception):
    pass

class WallpaperInvalidFormatException(Exception):
    pass

class IncorrectPasswordException(Exception):
    pass

class NotAllowedToModifyException(Exception):
    pass

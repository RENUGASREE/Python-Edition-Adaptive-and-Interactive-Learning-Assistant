from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password must contain at least %(min_length)d characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("This password must contain at least 1 digit."),
                code='password_no_digit',
            )
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _("This password must contain at least 1 letter."),
                code='password_no_letter',
            )
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("This password must contain at least 1 uppercase letter."),
                code='password_no_upper',
            )
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("This password must contain at least 1 lowercase letter."),
                code='password_no_lower',
            )
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>/?`~' for char in password):
            raise ValidationError(
                _("This password must contain at least 1 special character."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters, "
            "including at least 1 digit, 1 letter, 1 uppercase letter, 1 lowercase letter, "
            "and 1 special character."
        ) % {'min_length': self.min_length}

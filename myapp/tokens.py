# Importing the necessary modules/classes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# Define a custom TokenGenerator class that inherits from PasswordResetTokenGenerator
class TokenGenerator(PasswordResetTokenGenerator):
    # Override the _make_hash_value method from PasswordResetTokenGenerator
    def _make_hash_value(self, user, timestamp):
        # Concatenate the user's primary key (pk) and timestamp, converting them to text
        # This concatenation creates a unique string representing the user and the time
        return (
            text_type(user.pk) + text_type(timestamp)
        )

# Instantiate an object of the custom TokenGenerator class
generate_token = TokenGenerator()

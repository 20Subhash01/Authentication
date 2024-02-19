# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server address
EMAIL_HOST_USER = 'your-email@gmail.com'  # Email address used for sending emails
EMAIL_HOST_PASSWORD = 'your-email-password'  # Password for the email account
EMAIL_PORT = 587  # Port number for SMTP
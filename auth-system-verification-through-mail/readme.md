# Flask Authentication System with Email Verification

## Overview

This is a Flask-based authentication system that includes functionalities for user registration, login, and email verification. It uses PostgreSQL as the database, Flask-Mail for email functionalities, and integrates Google OAuth for additional authentication options. The system sends verification emails to users and includes a route for testing email functionality.

## Features

- User registration with email verification
- User login with password hashing
- Email sending for account verification
- Google OAuth integration for login
- Email testing route

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/auth-system-verification-through-mail.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd auth-system-verification-through-mail
   ```

3. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add the following environment variables:

   ```env
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgresql://username:password@localhost/your_database
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_email_password
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration
   OAUTHLIB_INSECURE_TRANSPORT=True
   OAUTHLIB_RELAX_TOKEN_SCOPE=True
   ```

6. **Initialize the Database**

   ```bash
   flask db upgrade
   ```

7. **Run the Application**

   ```bash
   python run.py
   ```

## Usage

- **Register**: Access the registration page at `/register` to create a new account.
- **Login**: Access the login page at `/login` to authenticate with your credentials.
- **Verify Email**: After registration, a verification email will be sent to your email address. Click the link in the email to activate your account.
- **Google OAuth Login**: Use Google OAuth to log in via `/login` (Google authentication) and handle the callback at `/oauth2callback`.

## Future Enhancements

The following functionalities are planned for future updates:

- **OTP (One-Time Password) Validation**: Add OTP-based validation to enhance security during the login and registration processes.
- **Email Approval**: Implement additional email approval steps to further secure account verification and user authentication.

## `.gitignore`

This repository includes a `.gitignore` file to exclude certain files and directories from being tracked by Git. The `.gitignore` file is configured to ignore:

- `.venv` - Virtual environment directory
- `.DS_Store` - macOS system file
- `auth-system-verification-through-mail/credentials.json` - Google credentials file
- `auth-system-verification-through-mail/.env` - Environment configuration file

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues and submit pull requests for improvements or bug fixes.

## Contact

For any questions or comments, please reach out to [shreyashmeshram0031@gmail.com](mailto:shreyashmeshram0031@gmail.com).
import bcrypt
import jwt
from flask import current_app as app, render_template

from src.factories.token import (ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE,
                                 SIGNUP_TOKEN_TYPE, TokenFactory)
from src.mail import Mail
from src.repos.signup import SignupRepo
from src.repos.user import UserRepo


class SignupService:
    def __init__(self, repo: SignupRepo, user_repo: UserRepo, mail: Mail):
        self._repo = repo
        self._user_repo = user_repo
        self._mail = mail

    def create_or_update(self, data):
        with self._repo.session() as s:
            signup = self._repo.get_first_by_email(data['email'], session=s)

            if signup:
                return self._repo.update_signup(signup.id, data['name'], data['password'], session=s)

            if self._user_repo.is_email_used(data['email'], session=s):
                raise self.SameEmail()

            return self._repo.create_signup(data['name'], data['email'], data['password'], session=s)

    def create_and_send(self, data, language=None):
        signup = self.create_or_update(data)

        link = app.config.get('HOST') + '/auth/register/confirm?token=' + \
            TokenFactory.create(SIGNUP_TOKEN_TYPE, signup)

        title = 'Hello!' if language.name == 'en' else 'Привет!'
        description = 'You\'re almost eye8 user. Click to the button to proceed.' if language.name == 'en' else 'Вы всего в шаге от того, чтобы стать пользователем eye8. Нажмите на кнопку, чтобы продолжить.'
        link_text = 'Complete registration' if language.name == 'en' else 'Завершить регистрацию'
        preheader = 'Signup at eye8.kg' if language.name == 'en' else 'Регистрация на eye8.kg'
        subject = link_text
        body = render_template(
            'link_email.html', 
            link=link,
            title=title,
            description=description,
            link_text=link_text,
            preheader=preheader
        )

        self._mail.send(subject, body, [signup.user_email])

    def confirm(self, token):
        with self._repo.session() as s:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'])
            signup = self._repo.get_first_by_email(
                decoded_token['user_email'], session=s)
            if signup is None:
                raise self.SignupNotFound()

            self._user_repo.create_user(
                signup.user_name, signup.user_email, signup.user_password, session=s)

            self._repo.delete(signup.id, session=s)

    class SameEmail(Exception):
        pass

    class SignupNotFound(Exception):
        pass

"""Unit tests for language automatic and manual selection."""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import translation
from django.utils.importlib import import_module
from django.test import TestCase

from i18nurl.settings import I18N_REDIRECT_URL_NAME, I18N_LANGUAGES


class I18nTestCase(TestCase):
    """Base class for posbox.i18n tests classes."""
    def setUp(self):
        """Common setup for all test methods:

        * Assigns self.guess_language_url and self.set_language_url.

        """
        super(I18nTestCase, self).setUp()
        self.guess_language_url = reverse('guess_language')
        self.set_language_url = reverse('set_language')
        self.default_language = settings.LANGUAGE_CODE
        for language_code, language_name in settings.LANGUAGES:
            if language_code != settings.LANGUAGE_CODE:
                self.other_language = language_code
                break
        with translation.override(self.default_language):
            url_name = I18N_REDIRECT_URL_NAME
            self.default_redirect_url = reverse(url_name)
        with translation.override(self.other_language):
            self.other_redirect_url = reverse(I18N_REDIRECT_URL_NAME)

    def set_language(self, language_code, redirect_url=None, temporary=False,
                     **kwargs):
        """Perform a set_language request with self.client and return
        response."""
        data = {'language': language_code}
        if redirect_url:
            data['next'] = redirect_url
        if temporary:
            data['temporary'] = 1
        return self.client.post(self.set_language_url, data, **kwargs)

    def set_session_language(self, language):
        """Set session's django_language to language. Creates a new session
        instance if necessary."""
        if settings.SESSION_COOKIE_NAME in self.client.cookies:
            session = self.client.session
        else:  # Create a new session.
            engine = import_module(settings.SESSION_ENGINE)
            session = engine.SessionStore()
            session.create()
            key = session._session_key
            self.client.cookies[settings.SESSION_COOKIE_NAME] = key
        session['django_language'] = language
        session.save()

    def assertI18nRedirection(self, response, redirect_url=None, msg=None):
        """Assert response is a redirection to redirect_url.

        .. note:: response must have been fetched with ``follow=True``.

        If ``redirect_url`` is None, it defaults to self.default_redirect_url.

        """
        # We don't use self.assertRedirects() because it checks the status code
        # of the response at the end of the redirection chain. The status code
        # at the end of the redirection chain is supposed to be tested as of
        # another's view test suite, i.e. it's not in the scope of current
        # method. In fact, right here, we don't know the status code to expect!
        # As an example, the first redirection could lead to the homepage,
        # which could be HTTP 200 or HTTP 301 depending on the implementation.
        if redirect_url is None:
            redirect_url = self.default_redirect_url
        redirection = ('http://testserver%s' % redirect_url, 302)
        args = []
        if msg is not None:
            args.append(msg)
        self.assertEqual(response.redirect_chain[0], redirection, *args)


class GuessLanguageTestCase(I18nTestCase):
    """Test automatic language detection."""
    def test_no_guess(self):
        """Without data to guess (user preferences, session, cookies or
        HTTP_ACCEPT_LANGUAGE header), the guess_language view redirects to
        to the default language website, with a message."""
        response = self.client.get(self.guess_language_url, follow=True)
        self.assertI18nRedirection(response)

    def test_guess_http_accept_language(self):
        """With HTTP_ACCEPT_LANGUAGE header only, the guess_language view
        redirects to the right website."""
        response = self.client.get(self.guess_language_url,
                                   HTTP_ACCEPT_LANGUAGE=self.other_language,
                                   follow=True)
        self.assertI18nRedirection(response, self.other_redirect_url)

    def test_guess_cookie(self):
        """With a language cookie only, then the guess_language view redirects
        to the right website."""
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = self.other_language
        response = self.client.get(self.guess_language_url, follow=True)
        self.assertI18nRedirection(response, self.other_redirect_url)

    def test_guess_session(self):
        """With a language set in session only, then the guess_language view
        redirects to the right website."""
        self.set_session_language(self.other_language)
        response = self.client.get(self.guess_language_url, follow=True)
        self.assertI18nRedirection(response, self.other_redirect_url)

    def test_detection_order(self):
        """Language detection is performed in the order specified in
        settings."""
        # Alternatives are sorted by priority. "user_profile" has precedence
        # over "session", which has precedence over "cookie", ...
        alternatives = ['session', 'cookie',
                        'http_accept_language', 'default']
        # For each pair of alternatives, we setup the client to request
        # the "other" language using the "major" alternative, and, at the
        # same time, request the "default" language using the "minor"
        # alternative.
        for i in range(0, len(alternatives)):
            # Reset request parameters.
            request_kwargs = {}
            self.client.cookies.clear()
            redirect_url = self.other_redirect_url
            major = alternatives[i]
            try:
                minor = alternatives[i + 1]
            except IndexError:
                break
            # Setup request with major alternative.
            if major == 'session':
                self.set_session_language(self.other_language)
            elif major == 'cookie':
                self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = self.other_language
            elif major == 'http_accept_language':
                request_kwargs['HTTP_ACCEPT_LANGUAGE'] = self.other_language
            elif major == 'default':
                # In that particular case, we expect that we are redirected to
                # the default website.
                redirect_url = self.default_redirect_url
            # Setup request with minor alternative.
            if minor == 'session':
                self.set_session_language(self.default_language)
            elif minor == 'cookie':
                self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = self.default_language
            elif minor == 'http_accept_language':
                request_kwargs['HTTP_ACCEPT_LANGUAGE'] = self.default_language
            elif minor == 'default':
                pass
            response = self.client.get(self.guess_language_url,
                                       follow=True,
                                       **request_kwargs)
            error_msg = 'Language detection failed: "%(major)s" detection ' \
                        'does not have precedence over "%(minor)s"' \
                        % {'major': major, 'minor': minor}
            self.assertI18nRedirection(response, redirect_url, error_msg)


class SetLanguageTestCase(I18nTestCase):
    """Test language change actions."""
    def test_language_list(self):
        """Called without arguments and without POST, set_language view
        displays a list of available languages."""
        response = self.client.get(self.set_language_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'i18n/set_language.html')

    def test_redirection(self):
        """Called with language argument, set_language view redirects to the
        website with specified language activated."""
        data = {'language': self.other_language}
        response = self.client.post(self.set_language_url, data, follow=True)
        self.assertI18nRedirection(response, self.other_redirect_url)

    def test_language_setting(self):
        """After a "set_language", "guess_language" detects the language that
        was just set."""
        # Call "set_language" with a language which is not the default.
        response = self.set_language(self.other_language, follow=True)
        self.assertI18nRedirection(response, self.other_redirect_url)
        # Then call "guess_language": the previously set language should be
        # detected.
        response = self.client.get(self.guess_language_url, follow=True)
        self.assertI18nRedirection(response, self.other_redirect_url)

    def test_temporary_redirection(self):
        """Called with "temporary" argument to True, set_language view doesn't
        remember the selected language in user profile, session, cookies..."""
        # Call "set_language" with a language which is not the default.
        response = self.set_language(self.other_language, temporary=True,
                                     follow=True)
        self.assertI18nRedirection(response, self.other_redirect_url)
        # Then call "guess_language": the default language should be detected.
        response = self.client.get(self.guess_language_url, follow=True)
        self.assertI18nRedirection(response, self.default_redirect_url)


class I18nURLTestCase(I18nTestCase):
    """Test localized URL patterns."""
    def test_i18n_url(self):
        """set_language and guess_language URL aren't localized."""
        for view_name in 'set_language', 'guess_language':
            with translation.override(self.default_language):
                default_url = reverse(view_name)
            with translation.override(self.other_language):
                other_url = reverse(view_name)
            self.assertEqual(default_url, other_url)

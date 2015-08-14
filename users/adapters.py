
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class ProfileAdapter(DefaultSocialAccountAdapter):

    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        """
        Hook that can be used to further populate the user instance.
        For convenience, we populate several common fields.
        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.
        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        return super(ProfileAdapter, self).populate_user(request, sociallogin, data)
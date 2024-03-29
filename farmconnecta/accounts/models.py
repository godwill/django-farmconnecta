from allauth.socialaccount.models import SocialAccount
import hashlib
from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    mobile_number = models.CharField(max_length=8, blank=True)
    follows = models.ManyToManyField(User, blank=True, related_name='follows')
    Producer = 'Producer'
    Buyer = 'Buyer'
    Pro = 'Pro Account'
    user_type_choices = (
        (Producer, 'Farmer'),
        (Buyer, 'Buyer'),
        (Pro, 'Pro Account'),
    )
    user_type = models.CharField(
        max_length=255,
        choices=user_type_choices,
        default=Buyer,
    )

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

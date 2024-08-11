from django.test import TestCase
from django.urls import reverse,resolve
from main.views import *

class TestURLS(TestCase):
    def setUp(self):
        self.homeurl = reverse('home')
        self.likeurl = reverse('like',args=['some-str'])
        self.commenturl = reverse('comment',args=['some-str'])
        self.createposturl = reverse('create')
        self.profileurl = reverse('profile',args=['some-str'])
        self.followurl = reverse('follow',args=['some-str'])
        self.deleteposturl = reverse('delete',args=['some-str'])
        self.searchurl = reverse('search')
        self.profileseturl = reverse('profilesettings')
    def test_home(self):
        return self.assertEquals(resolve(self.homeurl).func,index)
    def test_like(self):
        return self.assertEquals(resolve(self.likeurl).func,like)
    def test_comment(self):
        return self.assertEquals(resolve(self.commenturl).func,comment)
    def test_createpost(self):
        return self.assertEquals(resolve(self.createposturl).func,create_post)
    def test_profile(self):
        return self.assertEquals(resolve(self.profileurl).func,profile)
    def test_follow(self):
        return self.assertEquals(resolve(self.followurl).func,follow)
    def test_deletepost(self):
        return self.assertEquals(resolve(self.deleteposturl).func,delete_post)
    def test_search(self):
        return self.assertEquals(resolve(self.searchurl).func,search)
    def test_profilesettings(self):
        return self.assertEquals(resolve(self.profileseturl).func,profilesettings)

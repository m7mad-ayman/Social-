from django.test import TestCase , Client
from os import path
from django.test import TestCase
from django.core.files import File
from django.urls import reverse
from main.models import *
from account.models import *
from main.views import *

class TestVIEWS(TestCase):
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
        self.User =get_user_model()
        self.user1 = self.User.objects.create(username="testuser")
        self.user1.set_password("1234")
        self.user1.save()
        self.user2 = self.User.objects.create(username="testuser2")
        self.user2.set_password("1234")
        self.user2.save()
        self.profile1=Profile.objects.create(user=self.user1)
        self.profile2=Profile.objects.create(user=self.user2)

        self.client = Client()        
        
    def test_home(self):
        login=self.client.login(username = "testuser",password="1234")
        self.assertTrue(login)
        response= self.client.get(self.homeurl)
        #print(response)
        self.assertTemplateUsed(response,'index.html')
    def test_createpost(self):
        login=self.client.login(username = "testuser",password="1234")
        newPhoto =open(path.join("static/tests/", "test.jpg"), "rb")
        response = self.client.post(self.createposturl,{"picture":File(newPhoto, name=newPhoto.name),"caption":"test caption"})
        self.profile1.refresh_from_db()
        self.assertEquals(self.profile1.posts,1)
        return self.assertEquals(Post.objects.get(profile=self.profile1).caption,"test caption")
    def test_like(self):
        login=self.client.login(username = "testuser2",password="1234")
        newPhoto =open(path.join("static/tests/", "test.jpg"), "rb")
        post = Post.objects.create(profile=self.profile2,image=File(newPhoto, name=newPhoto.name),caption="test caption")
        response=self.client.post(reverse('like',args=[post.id]))
        post.refresh_from_db()
        return self.assertEquals(post.likes,1)
    def test_comment(self):
        login=self.client.login(username = "testuser2",password="1234")
        newPhoto =open(path.join("static/tests/", "test.jpg"), "rb")
        post = Post.objects.create(profile=self.profile2,image=File(newPhoto, name=newPhoto.name),caption="test caption")
        response=self.client.post(reverse('comment',args=[post.id]),{"comment":"test comment"})
        post.refresh_from_db()
        self.assertEquals(post.no_comments,1)
        return self.assertEquals(Relation.objects.get(relatedpost=post).relatedcom.comment,"test comment")
    def test_profiles_view(self):
        login=self.client.login(username = "testuser",password="1234")
        response1 =self.client.get(reverse("profile",args=[self.user1.username]))
        self.assertEquals(response1.status_code,302)
        response2 = self.client.get(reverse("profile",args=[self.user2.username]))
        return self.assertTemplateUsed(response2,"profile.html")
    def test_follow_and_unfollow(self):
        login=self.client.login(username = "testuser",password="1234")
        response = self.client.post(reverse("follow",args=[self.user2.username]))
        self.profile2.refresh_from_db()
        self.profile1.refresh_from_db()
        self.assertEquals(Follow.objects.get(follower=self.user1,followed=self.user2).value,"Following")
        self.assertEquals(self.profile2.followers,1)
        self.assertEquals(self.profile1.following,1)
        response = self.client.post(reverse("follow",args=[self.user2.username]))
        self.profile2.refresh_from_db()
        self.profile1.refresh_from_db()
        
        self.assertEquals(self.profile2.followers,0)
        self.assertEquals(self.profile1.following,0)
    def test_deletepost(self):
        login=self.client.login(username = "testuser2",password="1234")
        newPhoto =open(path.join("static/tests/", "test.jpg"), "rb")
        post = Post.objects.create(profile=self.profile2,image=File(newPhoto, name=newPhoto.name),caption="test caption")
        self.profile2.refresh_from_db()
        self.client.get(reverse("delete",args=[post.id]))
        return self.assertFalse(Post.objects.filter(profile=self.profile2).exists())
    def test_search(self):
        login=self.client.login(username = "testuser",password="1234")
        response=self.client.post(reverse("search"),{"searchvalue":"testuser2"})
        return self.assertTemplateUsed(response,"search.html")
    def test_profilesettings_with_data(self):
        login=self.client.login(username = "testuser",password="1234")
        newPhoto =open(path.join("static/tests/", "test.jpg"), "rb")
        response = self.client.post(reverse('profilesettings'),{"picture":File(newPhoto, name=newPhoto.name),"bio":"my bio"})
        self.profile1.refresh_from_db()
        self.assertEquals(self.profile1.bio,"my bio")
        return self.assertNotEquals(self.profile1.img.url,"media/img/24/profile.png")
    def test_profilesettings_without_data(self):
        login=self.client.login(username = "testuser",password="1234")
        response = self.client.post(reverse('profilesettings'))
        self.assertEquals(self.profile1.bio,"Your bio on social media")
        return self.assertEquals(self.profile1.img.url,"/media/media/img/24/profile.png")

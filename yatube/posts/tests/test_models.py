from django.test import TestCase

from ..models import Group, Post, User


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_name')
        cls.group = Group.objects.create(
            title='test_title_group',
            slug='test_slug_group',
            description='test_description',
        )
        cls.post = Post.objects.create(
            text='Text' * 5,
            author=cls.user,
            group=cls.group
        )

    def test_models_have_correct_object_names(self):
        group = PostsModelTest.group
        post = PostsModelTest.post
        expected_names = {
            group: group.title,
            post: post.text[:15],
        }
        for obj, expected in expected_names.items():
            with self.subTest(obj=obj):
                self.assertEqual(str(obj), expected)

from django.core.paginator import Page
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..helpers import LIMIT
from ..models import Group, Post, User


class ViewsTest(TestCase):
    # Check paginator
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.client = Client()
        cls.client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='test_title',
            slug='test-slug',
            description='test_description',
        )
        cls.post = Post.objects.create(
            text='word ' * 5,
            author=cls.user,
            group=cls.group
        )
        for i in range(LIMIT):
            Post.objects.create(
                text=f'Text {i + 2} post',
                author=cls.user,
                group=cls.group
            )
        cls.path_names = [
            'index',
            'group_list',
            'profile',
            'post_detail',
            'post_create',
            'post_edit',
        ]
        cls.urls = [
            reverse('posts:index'),
            reverse('posts:group_list', args=[cls.group.slug]),
            reverse('posts:profile', args=[cls.user.username]),
            reverse('posts:post_detail', args=[cls.post.pk]),
            reverse('posts:post_create'),
            reverse('posts:post_edit', args=[cls.post.pk]),
        ]
        cls.paths = {
            name: url for name, url in zip(cls.path_names, cls.urls)
        }

    def test_pages_uses_correct_template(self):
        templates = [
            'posts/index.html',
            'posts/group_list.html',
            'posts/profile.html',
            'posts/post_detail.html',
            'posts/create_post.html',
            'posts/create_post.html',
        ]
        path_templates = {
            name: template for name, template in zip(
                ViewsTest.path_names, templates
            )
        }
        for path_name, url in ViewsTest.paths.items():
            with self.subTest(url=url):
                responce = ViewsTest.client.get(url)
                self.assertTemplateUsed(
                    responce,
                    path_templates.get(path_name)
                )

    def test_pages_show_correct_context(self):
        context_pages = [
            {'page_obj': list(Post.objects.all()[:LIMIT])},
            {'group': ViewsTest.group,
             'page_obj': list(ViewsTest.group.posts.all()[:LIMIT])},
            {'author': ViewsTest.user,
             'page_obj': list(ViewsTest.user.posts.all()[:LIMIT])},
            {'post': ViewsTest.post},
            {'form': PostForm()},
            {'form': PostForm(instance=ViewsTest.post),
             'is_edit': True},
        ]
        path_context_pages = {
            name: context for name, context in zip(
                ViewsTest.path_names, context_pages
            )
        }
        for path_name, context in path_context_pages.items():
            responce = ViewsTest.client.get(ViewsTest.paths.get(path_name))
            for key, expected in context.items():
                with self.subTest(url=ViewsTest.paths.get(path_name), key=key):
                    self.assertIn(
                        key,
                        responce.context,
                        f'Key {key} not found in context page'
                    )
                    value = responce.context.get(key)
                    if key == 'form':
                        self.assertIsInstance(value, PostForm)
                        for field in PostForm.declared_fields.keys():
                            self.assertEqual(value.field, expected.field)
                    else:
                        if key == 'page_obj':
                            self.assertIsInstance(value, Page)
                            value = value.object_list
                        self.assertEqual(value, expected)

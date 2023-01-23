from django.test import TestCase

from ..models import Group, Post, User


class PostsGroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test title group',
            slug='test slug group',
            description='test description',
        )

    def test_model_have_correct_object_name(self):
        expected_name = PostsGroupModelTest.group.title
        self.assertEqual(str(PostsGroupModelTest.group), expected_name)

    def test_verbose_name(self):
        field_verboses = {
            'title': 'Заголовок',
            'description': 'Описание',
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    (PostsGroupModelTest.group._meta.get_field(field)
                     .verbose_name),
                    expected
                )

    def test_help_text(self):
        field_help_texts = {
            'title': 'Введите название группы',
            'description': 'Введите описание группы',
        }
        for field, expected in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    (PostsGroupModelTest.group._meta.get_field(field)
                     .help_text),
                    expected
                )


class PostsPostModelTest(TestCase):
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
            text='word ' * 5,
            author=cls.user,
            group=cls.group
        )

    def test_model_have_correct_object_name(self):
        expected_name = PostsPostModelTest.post.text[:15]
        self.assertEqual(str(PostsPostModelTest.post), expected_name)

    def test_verbose_name(self):
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    (PostsPostModelTest.post._meta.get_field(field)
                     .verbose_name),
                    expected
                )

    def test_help_text(self):
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PostsPostModelTest.post._meta.get_field(field).help_text,
                    expected
                )

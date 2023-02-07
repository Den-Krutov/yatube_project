from django.test import TestCase

from ..models import Comment, Group, Post, User


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test title group',
            slug='test slug group',
            description='test description',
        )

    def test_model_have_correct_object_name(self):
        expected_name = GroupModelTest.group.title
        self.assertEqual(str(GroupModelTest.group), expected_name)

    def test_verbose_name(self):
        field_verboses = {
            'title': 'Заголовок',
            'description': 'Описание',
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    (GroupModelTest.group._meta.get_field(field)
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
                    (GroupModelTest.group._meta.get_field(field)
                     .help_text),
                    expected
                )


class PostModelTest(TestCase):
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
        expected_name = PostModelTest.post.text[:15]
        self.assertEqual(str(PostModelTest.post), expected_name)

    def test_verbose_name(self):
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
            'image': 'Картинка',
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    (PostModelTest.post._meta.get_field(field)
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
                    PostModelTest.post._meta.get_field(field).help_text,
                    expected
                )


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_name')
        cls.post = Post.objects.create(
            text='Text post',
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Text comment',
        )

    def test_verbose_name(self):
        field_verboses = {
            'post': 'Пост',
            'author': 'Автор',
            'text': 'Текст комментария',
            'created': 'Дата публикации',
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    (CommentModelTest.comment._meta.get_field(field)
                     .verbose_name),
                    expected
                )

    def test_help_text(self):
        self.assertEqual(
            CommentModelTest.comment._meta.get_field('text').help_text,
            'Введите текст комментария'
        )

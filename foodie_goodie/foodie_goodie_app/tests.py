from django.forms import ValidationError
from django.test import TestCase
from .models import ListaZakupow, ElementListy, Jednostka, Uzytkownik, Forum, Post
from django.utils import timezone
from django.urls import reverse
from .forms.post_form import PostForm, ThreadForm
from django.core.files.uploadedfile import SimpleUploadedFile

class ShoppingListModelTests(TestCase):
    def setUp(self):
        # test user and unit
        self.user = Uzytkownik.objects.create(
            idUzytkownik = 1,
            nazwaUzytkownika="test_user",
            email="testuser@example.com",
            haslo="password123"
        )
        self.jednostka = Jednostka.objects.create(idJednostka=1, nazwaJednostki="g")
        
        # test shopping list
        self.lista = ListaZakupow.objects.create(
            nazwaListy="Moja Testowa Lista",
            autor=self.user
        )

    def test_create_lista_zakupow(self):
        """Test tworzenia listy zakupów."""
        self.assertEqual(ListaZakupow.objects.count(), 1)
        self.assertEqual(self.lista.nazwaListy, "Moja Testowa Lista")
        self.assertEqual(self.lista.autor, self.user)

    def test_add_element_to_lista(self):
        """Test dodawania elementu do listy zakupów."""
        element = ElementListy.objects.create(
            lista=self.lista,
            nazwaElementu="Jabłka",
            ilosc=5,
            jednostka=self.jednostka
        )
        self.assertEqual(ElementListy.objects.count(), 1)
        self.assertEqual(element.nazwaElementu, "Jabłka")
        self.assertEqual(element.ilosc, 5)
        self.assertEqual(element.jednostka, self.jednostka)



class ShoppingListViewTests(TestCase):
    def setUp(self):
        # test user and unit
        self.user = Uzytkownik.objects.create(
            idUzytkownik = 1,
            nazwaUzytkownika="test_user",
            email="testuser@example.com",
            haslo="password123"
        )
        self.jednostka = Jednostka.objects.create(idJednostka=1, nazwaJednostki="g")

        # test list
        self.lista = ListaZakupow.objects.create(
            nazwaListy="Moja Testowa Lista",
            autor=self.user
        )

        # test list element
        self.element = ElementListy.objects.create(
            lista=self.lista,
            nazwaElementu="Pomarancze",
            ilosc=3,
            jednostka=self.jednostka
        )

    def test_shopping_list_all_view(self):
        """Test widoku wszystkich list zakupów."""
        url = reverse('shopping_list_all')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moja Testowa Lista")
        self.assertTemplateUsed(response, "shopping_list/shopping_list_all.html")

    def test_shopping_list_detail_view(self):
        """Test widoku szczegółowego listy zakupów."""
        url = reverse('shopping_list_detail', args=[self.lista.idLista])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moja Testowa Lista")
        self.assertContains(response, "Pomarancze")
        self.assertTemplateUsed(response, "shopping_list/shopping_list_detail.html")

    def test_shopping_list_create_view(self):
        """Test tworzenia nowej listy zakupów."""
        url = reverse('shopping_list_create')
        data = {'nazwaListy': 'Nowa Lista', 'autor': self.user}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ListaZakupow.objects.count(), 2)
        self.assertTrue(ListaZakupow.objects.filter(nazwaListy="Nowa Lista").exists())


class ForumModelTest(TestCase):

    def setUp(self):
        self.user = Uzytkownik.objects.create(
            idUzytkownik = 1,
            nazwaUzytkownika="test_user",
            email="testuser@example.com",
            haslo="password123"
        )
        self.forum = Forum.objects.create(
            tytulForum="Test Forum",
            uzytkownik=self.user
        )

    def test_forum_creation(self):
        forum = self.forum
        self.assertEqual(forum.tytulForum, "Test Forum")
        self.assertEqual(forum.uzytkownik.nazwaUzytkownika, "test_user")

    def test_data_zalozenia(self):
        # create a post for the forum
        post = Post.objects.create(
            trescPost="Test post",
            forum=self.forum,
            autor=self.user,
            dataDodaniaPostu=timezone.now(),
            glosy=0
        )
        self.assertIsNotNone(self.forum.data_zalozenia())



class PostModelTest(TestCase):

    def setUp(self):
        self.user = Uzytkownik.objects.create(
            idUzytkownik=1,
            nazwaUzytkownika="test_user",
            email="testuser@example.com",
            haslo="password123"
        )
        self.forum = Forum.objects.create(
            tytulForum="Test Forum",
            uzytkownik=self.user
        )
        self.post = Post.objects.create(
            trescPost="Test Post",
            forum=self.forum,
            autor=self.user,
            glosy=5
        )

    def test_post_creation(self):
        post = self.post
        self.assertEqual(post.trescPost, "Test Post")
        self.assertEqual(post.glosy, 5)

    def test_clean_obrazek_valid(self):
        # simulate a valid image file using the PostForm
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        form = PostForm(data={'trescPost': 'Test Post', 'obrazek': image})
        form.is_valid()
        self.assertIsNone(form.cleaned_data.get('obrazek'))

            
            
            
class PostFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            'trescPost': 'Test post content',
            'obrazek': SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        }

    def test_post_form_valid(self):
        form = PostForm(data=self.form_data)
        self.assertTrue(form.is_valid())


    def test_post_form_empty_content(self):
        self.form_data['trescPost'] = ''
        form = PostForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['trescPost'], ['This field is required.'])


class ThreadFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            'tytulForum': 'Test Forum Title',
            'trescPost': 'Test thread post content',
            'obrazek': SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        }

    def test_thread_form_valid(self):
        form = ThreadForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_thread_form_invalid_title_length(self):
        self.form_data['tytulForum'] = 'Test'
        form = ThreadForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['tytulForum'], ['Tytuł powinien mieć co najmniej 5 znaków.'])
        
        
        
class ForumViewTest(TestCase):

    def setUp(self):
        self.user = Uzytkownik.objects.create(
            idUzytkownik = 1,
            nazwaUzytkownika="test_user",
            email="testuser@example.com",
            haslo="password123"
        )
        self.forum = Forum.objects.create(
            idForum = 1,
            tytulForum="Test Forum",
            uzytkownik=self.user
        )
        self.url = reverse('forum_detail', kwargs={'pk': self.forum.idForum})

    def test_forum_detail_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum_detail.html')
        self.assertIn('forum', response.context)
        self.assertIn('form', response.context)


    def test_forum_all_view(self):
        response = self.client.get(reverse('forum_all'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/forum_all.html')
        self.assertIn('forums', response.context)

    def test_create_thread_view_get(self):
        response = self.client.get(reverse('new_forum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/new_forum.html')


            
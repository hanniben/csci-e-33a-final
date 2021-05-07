from django.test import Client, TestCase
from game.models import User, Game

# Create your tests here.
class GameTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username="test", password="test")
        c = Client()
        response = c.post("/login", {"username": "test", "password": "test"})
        for x in range(100):
            response = c.post("/new", {"mode": "True"})

        for y in range(100):
            response = c.post("/new", {"mode": "False"})

      


    def test_start_square(self):
        for game in Game.objects.all():
            self.assertEqual(game.squares[0], "3")


    def test_last_square(self):
        for game in Game.objects.all():
            self.assertEqual(game.squares[99], "0")

    
    def test_hole_easy(self):
        for game in Game.objects.filter(mode = True):
            self.assertEqual(game.squares.count('1'), 4)


    def test_hole_hard(self):
        for game in Game.objects.filter(mode = False):
            self.assertEqual(game.squares.count('1'), 8)


    def test_key_square(self):
        for game in Game.objects.all():
            self.assertEqual(game.squares.count('2'), 10)


from django.contrib import admin
from .models import User, Game, Square, Row

# Register your models here.

admin.site.register(User)

admin.site.register(Game)

admin.site.register(Square)

admin.site.register(Row)

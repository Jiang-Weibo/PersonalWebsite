from django.contrib import admin

# Register your models here.
from .models import User
from .models import Image
from .models import Music
from .models import Video
from .models import Document
admin.site.register(User)
admin.site.register(Image)
admin.site.register(Music)
admin.site.register(Video)
admin.site.register(Document)
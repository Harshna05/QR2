from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image , ImageDraw

# Create your models here.
class QR (models.Model):
    name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to = 'qr_code', blank = True)
    
    def __str__(self):
        return self.name
    
    def save (self , *args, **kwargs):
        qr_image = qrcode.make(self.name)
        canvas = Image.new('RGB', (310,310), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr_image)
        fname = f'qr_code-{self.name}-{self.id}qr.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname , File(buffer), save = False)
        canvas.close()
        super().save(*args, **kwargs)
    
    
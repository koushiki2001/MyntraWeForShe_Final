from django.db import models

class Sketch:
    idno:int
    name:str
    img:str
    ptype:str
    


# class Product:

#     def __init__(self,name,price,img):
#         self.ptag=[]
#         self.name=name
#         self.img=img
#         self.price=price


#     def appendTag(self,tag):
#         self.ptag.append(tag)

class SavedProducts(models.Model):
    name=models.CharField(max_length=200)
    price=models.FloatField(default=0.0)
    img=models.CharField(max_length=200)
    ptag=models.CharField(max_length=200)


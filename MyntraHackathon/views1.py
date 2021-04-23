from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from .models import Sketch,SavedProducts
import cv2 as cv

uploaded_file_url = ''
prodname = ''
prodPrice = ''

#The objects of the different styles' sketches
sketch1 = Sketch()
sketch1.name = 'Cape Top'
sketch1.id = 1001
sketch1.img = 'KaftanSketch.jpeg'
sketch1.ptype = "Cape"


sketch2 = Sketch()
sketch2.name = 'Spaghetti Top'
sketch2.id = 1002
sketch2.img = 'spag1.jpg'
sketch2.ptype = "Spaghetti"


sketch3 = Sketch()
sketch3.name = 'One Shoulder Ruffle Top'
sketch3.id = 1003
sketch3.img = 'top.jpg'
sketch3.ptype = "One Shoulder Ruffle Top"






savedProductsList=[]

#List of all the sketches 
product_Sketch = [sketch1,sketch2,sketch3]     


def open(request):
    # all_entries = SavedProducts.objects.all()
    # print(all_entries)
    # SavedProducts.objects.all().delete()
    # all_entries = SavedProducts.objects.all()
    # print(all_entries)
    return render(request,'index.html')



#Function to print all the products stored in the database
def view_products(request):
    all_entries = SavedProducts.objects.all()
    savedProductsList=list(all_entries)
    return render(request,'index-2.html',{'productsToBeDisplayed':savedProductsList})


#Function for adding a new product to the database
def simple_upload(request):
    global uploaded_file_url
    global prodname
    global prodPrice 

    #product_details are being uploaded
    if request.method == 'POST' and request.FILES['myfile']:
        prodname = request.POST['name']
        prodPrice = request.POST['price']
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'form2.html', {
        'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'form2.html')



#After filling the product details and uploading the image the product will be matched with the sketches stored 
#in the database and will be assigned a tag based on that.

def check_results(request):
    global uploaded_file_url
    global product_Sketch
    global prodname
    global prodPrice 
    global savedProductsList

    productsToBeDisplayed = []
    pathNew = 'C:/Users/Kaushiki/projects/myntra2'+uploaded_file_url
    prev=0
    pos=0
    for i in range(len(product_Sketch)):

        
        prodPath=product_Sketch[i].img
        ProductpathNew = 'C:/Users/Kaushiki/projects/myntra2/static/sketches/'+prodPath
        
        
        template_path = r"{}".format(pathNew)
        product_path=r"{}".format(ProductpathNew)
        

        imgg= cv.imread(template_path,0)

        
        
        img=imgg
        edges = cv.Canny(img,100,200)
        img = cv.imread(product_path,0)
        edges1 = cv.Canny(img,100,200)
        img = edges1
        img2 = img.copy()
        
        template=edges
        w, h = template.shape[::-1]
        
        methods = ['cv.TM_CCOEFF_NORMED']
        for meth in methods:
            img = img2.copy()
            method = eval(meth)
            area=1
            # Apply template Matching
            res = cv.matchTemplate(img,template,method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            # If the method is TM_COEFF_NORMED  take maximum
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            rec=cv.rectangle(img,top_left, bottom_right, (255,255,255), 2)
            
            
            #since we are using TM_COEFF_NORMED method so we consider the max_loc 
            #the sketch for which the max_loc is the least is considered to be
            #the right fit for the product and accordingly the product is being assigned a tag
            
            if(prev==0):
                prev=max_val
           
            if(max_val<0.05 and max_val<prev):
                
                pos=i

                
    entry=SavedProducts()
    entry.name=prodname
    entry.price=prodPrice
    entry.img=uploaded_file_url
    entry.ptag=product_Sketch[pos].ptype

    entry.save()

    #Printing the status of the database operation in the console
    print("\nProduct Saved Successfully\n")
    print("Product Name: ",prodname)
    print("Product Price: ",prodPrice)
    print("Product Tag: ",product_Sketch[pos].ptype)
    print('\n')
    all_entries = SavedProducts.objects.all()
   
    savedProductsList=list(all_entries)
    
                
                
        
    return render(request, 'index-2.html',{'productsToBeDisplayed':savedProductsList})

#Function which shows all the style sketches stored in the system
def showSketches(request):

    return render(request, 'sketches.html',{'allSketches':product_Sketch})


#When the user clicks on the view button attached to the sketches this function is invoked
#This function matches the tags assigned to the products by the system to the tags of the sketches
#and helps find the best fit products for the user.
def findTops(request):

    global savedProductsList

    productsToBeDisplayed = []
    receivedTag = request.POST["tag"]
    for i in savedProductsList:
        
        if(i.ptag == receivedTag):
            productsToBeDisplayed.append(i)
    
    return render(request, 'index-2.html',{'productsToBeDisplayed':productsToBeDisplayed})

    

    



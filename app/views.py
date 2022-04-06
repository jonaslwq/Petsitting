from django.shortcuts import render, redirect
from django.db import connection

# # Create your views here.
# def index(request):
#     """Shows the main page"""

#     ## Delete customer
#     if request.POST:
#         if request.POST['action'] == 'delete':
#             with connection.cursor() as cursor:
#                 cursor.execute("DELETE FROM customers WHERE customerid = %s", [request.POST['id']])

#     ## Use raw query to get all objects
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM customers ORDER BY customerid")
#         customers = cursor.fetchall()

#     result_dict = {'records': customers}

#     return render(request,'app/index.html',result_dict)


# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['dob'] , request.POST['since'], request.POST['customerid'], request.POST['country'] ])
                return redirect('index')    
            else:
                status = 'Customer with ID %s already exists' % (request.POST['customerid'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
    return render(request, "app/edit.html", context)

def main_page(request):
    """Shows the main page"""
    return render(request,'app/main_page.html')

def pending(request):
    """Shows the pending page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:

        cursor.execute("select * from pending where offerid in (select offerid from joboffer where petid in (select petid from pet where username = 'johnny123')) order by offerid") 
        pendingoffers = cursor.fetchall()

    result_dict = {'pendingrecords': pendingoffers}

    return render(request,'app/pending.html',result_dict)

def view_offer(request,offerid):
    """Shows the offer info page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM joboffer WHERE offerid = %s", [offerid])
        offer = cursor.fetchone()
    result_dict = {'pendingoffers': offer}

    return render(request,'app/view_offer.html',result_dict)

def view_user(request, username): 
    """Shows the user info page""" 
     
    ## Use raw query to get a customer 
    with connection.cursor() as cursor: 
        cursor.execute("SELECT * FROM portfolio WHERE username = %s", [username]) 
        user = cursor.fetchone() 
    result_dict = {'pendingusers': user} 
 
    return render(request,'app/view_user.html',result_dict)

def register_user(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if username is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM portfolio WHERE username = %s", [request.POST['username']])
            user = cursor.fetchone()
            ## No user with same username
            if user == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO portfolio VALUES (%s, %s, %s, %s, %s)"
                        , [request.POST['username'], request.POST['email'], request.POST['phonenum'],
                           request.POST['year_exp'] , request.POST['password'] ])
                return redirect('login')    
            else:
                status = 'User with username %s already exists' % (request.POST['username'])


    context['status'] = status
 
    return render(request, "app/register_user.html", context)

def register_pet(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if petid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM pet WHERE petid = %s", [request.POST['petid']])
            pet = cursor.fetchone()
            ## No pet with same petid
            if pet == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO pet VALUES (%s, %s, %s, %s, %s)"
                        , [request.POST['petname'], request.POST['petid'], request.POST['type'],
                           request.POST['breed'] , request.POST['username'] ])
                return redirect('index')    
            else:
                status = 'Pet with ID %s already exists' % (request.POST['petid'])


    context['status'] = status
 
    return render(request, "app/register_pet.html", context)

def mypets(request):
    """Shows the mypets page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:

        cursor.execute("SELECT * FROM pet WHERE username = 'johnny123'")
        animal = cursor.fetchall()

    result_dict = {'pets': animal}

    return render(request,'app/mypets.html',result_dict)

def sit_pet(request):
    """Shows the sit a pet page"""

    with connection.cursor() as cursor:
        cursor.execute("SELECT offerid, petid FROM joboffer WHERE petid NOT IN (SELECT petid FROM pet WHERE username = 'johnny123')")
        alloffers = cursor.fetchall()

    result_dict = {'total': alloffers}

    return render(request,'app/sit_pet.html', result_dict)

def view_pet(request, petid):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.petname, p.type, p.breed, j.date_from, j.date_to, j.location, j.price, p.petid FROM pet p, joboffer j WHERE p.petid = %s AND p.petid = j.petid", [petid])
        eachpet = cursor.fetchone()
    result_dict = {'allpet': eachpet}

    return render(request,'app/view_pet.html',result_dict)

def interested(request):
    """Shows the interested page"""
    return render(request,'app/interested.html')

def history(request):  
    """Shows the history page""" 
 
    ## Use raw query to get all objects 
    with connection.cursor() as cursor: 
        cursor.execute("SELECT * FROM joboffer j, transaction t WHERE t.username = 'johnny123' AND t.username = j.username AND t.offerid = j.offerid") 
        transactions = cursor.fetchall() 
 
    result_dict = {'history': transactions} 
 
    return render(request,'app/history.html',result_dict)

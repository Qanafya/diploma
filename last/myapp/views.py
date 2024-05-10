from django.shortcuts import render, get_object_or_404
from django.template import engine

from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.db.models import Subquery


@csrf_exempt
def signupchef(request):
    return render(request, 'signupchef.html')

@csrf_exempt
def register(request):
    form = ChefForm(request.POST)
    username = request.POST['username']
    if Chef.objects.filter(username=username).exists():
        print('username already taken')
        return redirect('/tyu/')
    else:
        try:
            form.save()
            print('chef created')
            return redirect('/login/')
        except:
            pass

@csrf_exempt
def loginchef(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        data = Chef.objects.filter(username=username)
        role = "chef"
        customer = Customer.objects.all()
        for q in data:
            if q.password == password:
                user = Chef.objects.get(username=username)
                if Jur.objects.filter(user_id = user.id).exists():
                    tek = Jur.objects.filter(user_id = user.id, role=role)
                    if tek.first().role != 'chef' and tek.last().role != 'chef':
                        form = Jur(user_id=user.id, role='chef')
                        form.save()
                else:
                    form = Jur(user_id = user.id, role='chef')
                    form.save()
                jurgen = Jur.objects.get(user_id=user.id, role='chef')
                chef = Chef.objects.get(id=jurgen.user_id)
                order = Order.objects.all()
                if Meal.objects.filter(chef_id=jurgen.user_id).exists():
                    meal = Meal.objects.filter(chef_id=jurgen.user_id)
                    if ChefDetail.objects.filter(chef_id=jurgen.user_id).exists():
                        detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
                        return render(request, 'chef_profile.html',                                           #asdasd
                                      {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'meal': meal, 'order': order, 'customer': customer})
                    else:
                        return render(request, 'chef_profile.html',
                                      {'jurgen': jurgen, 'chef': chef, 'meal': meal, 'order': order, 'customer': customer})
                elif ChefDetail.objects.filter(chef_id=jurgen.user_id).exists():
                    detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
                    return render(request, 'chef_profile.html',
                                  {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'order': order, 'customer': customer})
                return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'order': order, 'customer': customer})
    return redirect('/')


@csrf_exempt
def signupcustomer(request):
    if request.method == 'GET':
        return render(request, 'signupcustomer.html')
    elif request.method == 'POST':
        form = CustomerForm(request.POST)
        email = request.POST['email']
        if Customer.objects.filter(email=email).exists():
            print("email already used")
            return redirect('/signupcustomer/')
        else:
            if form.is_valid():
                try:
                    form.save()
                    print("customer created")
                    return redirect('/login/')
                except:
                    pass

@csrf_exempt
def logincustomer(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        role = "customer"
        data = Customer.objects.filter(email=email)
        for q in data:
            if q.password == password:
                user = Customer.objects.get(email=email)
                if Jur.objects.filter(user_id=user.id).exists():
                    tek = Jur.objects.filter(user_id=user.id, role=role)
                    if tek.first().role != 'customer' and tek.last().role != 'customer':
                        form = Jur(user_id=user.id, role='customer')
                        form.save()
                else:
                    form = Jur(user_id=user.id, role='customer')
                    form.save()
                user = Customer.objects.get(email=email)
                jurgen = Jur.objects.filter(role=role, user_id=user.id).first()
                print("jurgen " + str(jurgen))
                detail = ChefDetail.objects.all()
                if Meal.objects.all().exists():
                    meal = Meal.objects.all()
                    chef = Chef.objects.all()
                    return render(request, 'set.html', {'jurgen': jurgen, 'meal': meal, 'chef': chef, 'detail': detail})
                else:
                    return render(request, 'set.html', {'jurgen': jurgen, 'detail': detail})
            return redirect('/login/')

#Open login form
def login(request):
    return render(request, 'login.html')

def updatechef(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        jur_id = request.POST.get('jur')
        jurgen = Jur.objects.get(id=jur_id)
        chef = Chef.objects.get(id=jurgen.user_id)
        chef.first_name = first_name
        chef.last_name = last_name
        chef.email = email
        chef.address = address
        chef.save()
        order = Order.objects.all()
        if Meal.objects.filter(chef_id=jurgen.user_id).exists():
            meal = Meal.objects.filter(chef_id=jurgen.user_id)
            if ChefDetail.objects.filter(chef_id=jurgen.user_id).exists():
                detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
                return render(request, 'chef_profile.html',
                              {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'meal': meal, 'order': order})
            else:
                return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'meal': meal, 'order': order})
        elif ChefDetail.objects.filter(chef_id=jurgen.user_id).exists():
            detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
            return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'order': order})
        return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'order': order})


def updatedetail(request):
    if request.method == 'POST':
        about = request.POST.get('about')
        short = request.POST.get('short')
        speciality = request.POST.get('speciality')
        is_active = request.POST.get('is_active', False)
        service = request.POST.get('service')
        if service == None:
            print('asd ' + str(service))
        jurgen_id = request.POST.get('jur')
        jurgen = Jur.objects.get(id=jurgen_id)
        chef = Chef.objects.get(id=jurgen.user_id)
        if ChefDetail.objects.filter(chef_id=jurgen.user_id).exists():
            meal = Meal.objects.filter(chef_id=jurgen.user_id)
            detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
            detail.about = about
            detail.short = short
            detail.speciality = speciality
            detail.service = service
            detail.is_active = is_active == 'on'
            detail.save()
            order = Order.objects.all()
            if Meal.objects.filter(chef_id=jurgen.user_id).exists():
                meal = Meal.objects.filter(chef_id=jurgen.user_id)
                return render(request, 'chef_profile.html',
                              {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'meal': meal, 'order': order})
            else:
                return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'order': order})
        elif Meal.objects.filter(chef_id=jurgen.user_id).exists():
            meal = Meal.objects.filter(chef_id=jurgen.user_id)
            check = is_active == 'on'
            form = ChefDetail(chef_id=jurgen.user_id, about=about, short=short, speciality=speciality, is_active=check)
            form.save()
            detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
            return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'meal': meal, 'order': order})
        else:
            check = is_active == 'on'
            form = ChefDetail(chef_id=jurgen.user_id, about=about, short=short, speciality=speciality, is_active=check)
            form.save()
            detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
            return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'order': order})




def main_page(request):
    return render(request, 'main_page.html')

def addmeal(request):
    jurgen_id = request.POST.get('jur')
    jurgen = Jur.objects.get(id=jurgen_id)
    title = request.POST.get('title')
    category = request.POST.get('category')
    price = request.POST.get('price')
    desc = request.POST.get('desc')
    photo_link = request.POST.get('photo_link')
    ingredient = request.POST.get('ingredient')
    meal_id = request.POST.get('meal_id')
    order = Order.objects.all()
    if Meal.objects.filter(id=meal_id).exists():
        meals = Meal.objects.get(id=meal_id)
        meals.title = title
        meals.category = category
        meals.price = price
        meals.desc = desc
        meals.photo_link = photo_link
        meals.ingredient = ingredient
        meals.save()
    else:
        form = Meal(title=title, category=category, price=price, desc=desc, photo_link=photo_link, ingredient=ingredient, chef_id=jurgen.user_id)
        form.save()
    chef = Chef.objects.get(id=jurgen.user_id)
    if Meal.objects.filter(chef_id=jurgen.user_id).exists():
        meal = Meal.objects.filter(chef_id=jurgen.user_id)
        if ChefDetail.objects.filter(chef_id=jurgen.user_id).exists():
            detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
            return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'meal': meal, 'order': order})
        else:
            return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'meal': meal, 'order': order})
    elif ChefDetail.objects.filter(chef_id=jurgen.user_id).exists():
        detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
        return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'order': order})
    return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'order': order})


def addmealpage(request):
    jurgen_id = request.POST.get('jur')
    jurgen = Jur.objects.get(id=jurgen_id)
    return render(request, 'meal_new.html', {'jurgen': jurgen})

def deletemeal(request):
    jurgen_id = request.POST.get('jur')
    meal_id = request.POST.get('meal_id')
    jurgen = Jur.objects.get(id=jurgen_id)
    meal = Meal.objects.get(id=meal_id)
    meal.delete()
    chef = Chef.objects.get(id=jurgen.user_id)
    order = Order.objects.all()
    if Meal.objects.filter(chef_id=jurgen.user_id).exists():
        meal = Meal.objects.filter(chef_id=jurgen.user_id)
        if ChefDetail.objects.filter(chef_id=jurgen.user_id).exists():
            detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
            return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'meal': meal, 'order': order})
        else:
            return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'meal': meal, 'order': order})
    elif ChefDetail.objects.filter(chef_id=jurgen.user_id).exists():
        detail = ChefDetail.objects.get(chef_id=jurgen.user_id)
        return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'detail': detail, 'order': order})
    return render(request, 'chef_profile.html', {'jurgen': jurgen, 'chef': chef, 'order': order})

def changepage(request):
    jurgen_id = request.POST.get('jur')
    meal_id = request.POST.get('meal_id')
    jurgen = Jur.objects.get(id=jurgen_id)
    meal = Meal.objects.get(id=meal_id)
    return render(request, 'meal_new.html', {'meal': meal, 'jurgen': jurgen})

def signupchef(request):
    return render(request, 'signupchef.html')

def our_menu(request):
    return render(request, 'our_menu_n.html')

def header(request):
    return render(request, 'header.html')

def to_pay(request):
    jur = request.POST.get('jur')
    meal_id = request.POST.get('meal_id')
    jurgen = Jur.objects.get(id=jur)
    meal = Meal.objects.get(id=meal_id)
    return render(request, 'pay_order.html', {'meal': meal, 'jurgen': jurgen})

def meal(request, id):
    meal = Meal.objects.get(id=id)
    if request.method == 'POST':
        jurgen_id = request.POST.get('jur')
        jurgen = Jur.objects.get(id=jurgen_id)
        return render(request, 'meal.html', {'jurgen': jurgen, 'meal': meal})
    else:
        return render(request, 'meal.html', {'meal': meal})

def order(request):
    if request.method == 'POST':
        jurgen_id = request.POST.get('jur')
        meal_id = request.POST.get('meal_id')
        jurgen = Jur.objects.get(id=jurgen_id)
        meal = Meal.objects.get(id=meal_id)
        status = 'paid'
        form = Order(meal_id=meal_id, customer_id=jurgen.user_id, chef_id=meal.chef_id, status=status)
        form.save()
        order = Order.objects.filter(customer_id=jurgen.user_id)
        meal = Meal.objects.all()
        return render(request, 'customer_cart.html', {'jurgen': jurgen, 'order': order, 'meal': meal})
    else:
        return redirect('/login/')

def vieworder(request):
    if request.method == 'POST':
        jurgen_id = request.POST.get('jur')
        jurgen = Jur.objects.get(id=jurgen_id)
        order = Order.objects.filter(chef_id=jurgen.user_id)
        customer = Customer.objects.all()
        meal = Meal.objects.all()
        return render(request, 'chef_profile.html', {'jurgen': jurgen, 'order': order, 'customer': customer, 'meal': meal})

def chefprof(request):
    return render(request, 'chef_profile.html')

def old(request):
    return render(request, 'signupchef.html')


def process(request):
    return render(request, 'customer_cart.html')

def cart(request):
    return render(request, 'customer_cart.html')

def edit_profile_chef(request):
    if request.method == 'POST':
        id = request.get['id']
        jur = Jur.objects.get(id=id)
        chef_id = jur.user_id
        order = Order.objects.all()
        if jur.role == 'chef':
            detail = ChefDetail.objects.get(id=chef_id)
            chef = Chef.objects.get(id=chef_id)
            return render(request, 'chef_profile.html', {'jur': jur, 'detail': detail, 'chef': chef, 'order': order})
    else:
        return redirect('/login/')

def user_profile(request):
    return render(request, 'user_profile_n.html')

def menu(request):
    if request.method == 'POST':
        jurgen_id = request.POST.get('jur')
        jurgen = Jur.objects.get(id=jurgen_id)
        if Meal.objects.all().exists():
            meal = Meal.objects.all()
            chef = Chef.objects.all()
            return render(request, 'our_menu_n.html', {'jurgen': jurgen, 'meal': meal, 'chef': chef})
        else:
            return render(request, 'our_menu_n.html', {'jurgen': jurgen})
    else:
        if Meal.objects.all().exists():
            meal = Meal.objects.all()
            chef = Chef.objects.all()
            return render(request, 'our_menu_n.html', {'meal': meal, 'chef': chef})
        else:
            return render(request, 'our_menu_n.html')

def meals(request):
    if request.method == 'POST':
        jur = request.POST.get('jur')
        meal_id = request.POST.get('meal_id')
        jurgen = Jur.objects.get(id=jur)
        meal = Meal.objects.get(id=meal_id)
        return render(request, 'meal.html', {'jurgen': jurgen, 'meal': meal})


def set(request):
    return render(request, 'set.html')

def new(request):
    return render(request, 'new.html')

def test(request):
    return render(request, 'test.html')

def phone(request):
    return render(request, 'phone.html')
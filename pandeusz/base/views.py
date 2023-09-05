from django.shortcuts import render, redirect
from .models import Place, Topic, File
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PlaceForm, TopicForm, FileForm, CustomUserForm
from django.http import JsonResponse


def home(request):
    places = Place.objects.all()
    context = {'places': places}
    return render(request, 'base/home.html', context)


def place(request, pk):
    place = Place.objects.get(id=pk)
    topics = Topic.objects.filter(place=pk)
    context = {'place': place, 'topics': topics}
    return render(request, 'base/place.html', context)


def topic(request, place_id, topic_id):
    topic = Topic.objects.get(id=topic_id)
    place=Place.objects.get(id=place_id)
    otherTopics = Topic.objects.filter(place=place_id)
    files = File.objects.filter(topic=topic_id)
    context = {'topic': topic, 'files': files, "otherTopics": otherTopics, 'place': place}
    return render(request, 'base/topic.html', context)


@login_required(login_url='login')
def create_place(request):
    form = PlaceForm()
    if request.method == "POST":
        form = PlaceForm(request.POST)
        if form.is_valid():
            Place.objects.create(
                host=request.user,
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                isPrivate=True if form.data.get("status") == "on" else False,
                accessPassword=request.POST.get('accessPassword')

            )
            return redirect('home')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'base/place_form.html', context)


@login_required(login_url='login')
def create_topic(request, place_id):
    form = TopicForm()
    if request.method == "POST":
        form = TopicForm(request.POST)
        place = Place.objects.get(id=place_id)
        if form.is_valid():
            Topic.objects.create(
                place=place,
                name=request.POST.get('name'),
                description=request.POST.get('description'),
            )
            return redirect('home')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'base/topic_form.html', context)


@login_required(login_url='login')
def update_place(request, pk):
    place = Place.objects.get(id=pk)
    form = PlaceForm(instance=place)
    if request.method == "POST":
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            form.save()
            return redirect(f'/place/{place.id}')

    context = {'form': form}
    return render(request, 'base/place_form.html', context)


@login_required(login_url='login')
def update_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    form = TopicForm(instance=topic)
    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect(f'/place/{topic.place.id}/topic/{topic.id}')

    context = {'form': form}
    return render(request, 'base/topic_form.html', context)


@login_required(login_url='login')
def delete_place(request, pk):
    place = Place.objects.get(id=pk)
    if request.method == "POST":
        place.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': place})


@login_required(login_url='login')
def delete_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    if request.method == "POST":
        topic.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': topic})


@login_required(login_url='login')
def add_file(request, pk):
    topic = Topic.objects.get(id=pk)
    place = topic.place
    form = FileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            file = form.save(commit=False)
            file.topic = topic
            file.save()
            return redirect('topic', place_id=topic.place.id, topic_id=pk)

    return render(request, 'base/add_file.html', {'form': form, 'topic': topic, 'place': place})


def login_page(request):
    page = 'login'
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User doesn`t exist")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User or password doesn`t exist.")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect("home")


def register_user(request):
    if request.method != 'POST':
        form = CustomUserForm()
    else:
        print("Nie Post")
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def find(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    try:
        place = Place.objects.get(pk__icontains=q)

        return redirect(f"place/{place.pk}")
    except:
        return redirect("no-place")


def no_place(request):
    return render(request, 'base/no_place.html')


def place_password(request, pk):
    place = Place.objects.get(id=pk)
    print("NOsz kurwa pojaw się")
    if request.method == "POST":
        entered_password = request.POST.get("q")

        if entered_password == place.accessPassword:
            print("POPRAWNE")
            # Hasło jest poprawne, przenieś się do widoku miejsca
            return redirect(f'/place/{place.id}')
        else:
            print("Niepoprawne")
            # Hasło jest niepoprawne, możesz wykonać jakieś działania, np. wyświetlić komunikat
            context = {'place': place, 'message': 'Niepoprawne hasło'}
            return render(request, 'base/place_password.html', context)

    context = {'place': place}
    return render(request, 'base/place_password.html', context)


def delete_file(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        try:
            file_to_delete = File.objects.get(pk=file_id)
            file_to_delete.delete()
            return JsonResponse({'message': 'Plik został usunięty.'})
        except File.DoesNotExist:
            return JsonResponse({'error': 'Plik nie istnieje.'})
    return JsonResponse({'error': 'Niepoprawne żądanie.'})

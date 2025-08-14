from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.cache import never_cache

from django.contrib.auth.models import User
from .models import UserProfile, Internship, InternshipApplication, HouseProject, Firm, Client
from .forms import InternshipForm, InternshipApplicationForm, HouseProjectForm
from django.contrib.auth.decorators import login_required

def home(request):
    # If logged in and requesting "real home", just show it
    if request.GET.get("force"):
        return render(request, 'core/home.html')

    if request.user.is_authenticated:
        try:
            role = request.user.userprofile.role
            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'firm':
                try:
                    _ = request.user.firm
                    return redirect('firm_dashboard')
                except Firm.DoesNotExist:
                    messages.error(request, "Firm data missing.")
                    return redirect('logout')
            elif role == 'client':
                try:
                    _ = request.user.client
                    return redirect('client_dashboard')
                except Client.DoesNotExist:
                    messages.error(request, "Client data missing.")
                    return redirect('logout')
        except UserProfile.DoesNotExist:
            logout(request)
            return redirect('login')

    return render(request, 'core/home.html')


from django.db import transaction, IntegrityError

@never_cache
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role = request.POST['role']

        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {'error': 'Username already exists'})

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, password=password, email=email)
                UserProfile.objects.create(user=user, role=role)

                # Automatically create firm or client model
                if role == 'firm':
                    Firm.objects.create(user=user, name='Unnamed Firm', location='Unknown')
                elif role == 'client':
                    Client.objects.create(user=user, name=username)

            messages.success(request, "Account created successfully!")
            return redirect('login')
        except Exception as e:
            print(f"Registration error: {e}")
            return render(request, 'core/register.html', {'error': 'Error creating user. Please try again.'})

    return render(request, 'core/register.html')

@never_cache
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Redirect to the appropriate dashboard based on role
            try:
                role = user.userprofile.role
                if role == 'student':
                    return redirect('student_dashboard')
                elif role == 'firm':
                    return redirect('firm_dashboard')
                elif role == 'client':
                    return redirect('client_dashboard')
            except UserProfile.DoesNotExist:
                logout(request)
                messages.error(request, "Profile data missing.")
                return redirect('login')

        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def student_dashboard(request):
    internships = Internship.objects.all()

    # Filters
    search = request.GET.get('search')
    location = request.GET.get('location')
    mode = request.GET.get('mode')
    stipend = request.GET.get('stipend')

    if location:
        internships = internships.filter(location__icontains=location)
    if mode:
        internships = internships.filter(mode=mode)
    if stipend == 'paid':
        internships = internships.filter(stipend__gt=0)
    elif stipend == 'unpaid':
        internships = internships.filter(stipend=0)
    if search:
        internships = internships.filter(
            Q(title__icontains=search) |
            Q(company_name__icontains=search) |
            Q(description__icontains=search)
        )

    applications = InternshipApplication.objects.filter(student=request.user)
    applied_ids = applications.values_list('internship_id', flat=True)

    available_internships = internships.exclude(id__in=applied_ids)

    # For location filter dropdown
    locations = Internship.objects.values_list('location', flat=True).distinct()

    return render(request, 'core/student_dashboard.html', {
        'available_internships': available_internships,
        'applications': applications,
        'locations': locations,
    })


@login_required
def apply_internship(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)

    if request.method == 'POST':
        form = InternshipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.internship = internship
            application.student = request.user
            application.save()
            messages.success(request, "🎉 Application submitted successfully!")
            return redirect('student_dashboard')
        else:
            messages.error(request, "⚠️ Please correct the errors in the form.")
    else:
        form = InternshipApplicationForm()

    return render(request, 'core/apply_internship.html', {
        'internship': internship,
        'form': form
    })
@login_required
def firm_dashboard(request):
    # Ensure the user has a Firm profile
    firm, created = Firm.objects.get_or_create(
        user=request.user,
        defaults={'name': request.user.username + "'s Firm", 'location': 'Unknown'}
    )

    internships = Internship.objects.filter(firm=firm)
    applicants = InternshipApplication.objects.filter(internship__firm=firm)

    # Show projects that have not yet been approved by any firm
    projects = HouseProject.objects.filter(firm__isnull=True, status='pending')

    return render(request, 'core/firm_dashboard.html', {
        'internships': internships,
        'applicants': applicants,
        'projects': projects
    })

@login_required
def post_internship(request):
    firm = get_object_or_404(Firm, user=request.user)

    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.firm = firm
            internship.save()
            messages.success(request, "Internship posted successfully.")
            return redirect('firm_dashboard')
    else:
        form = InternshipForm()

    return render(request, 'core/post_internship.html', {'form': form})

@login_required
def delete_internship(request, internship_id):
    firm = get_object_or_404(Firm, user=request.user)
    internship = get_object_or_404(Internship, id=internship_id, firm=firm)

    if request.method == 'POST':
        internship.delete()
        messages.success(request, "Internship deleted.")
        return redirect('firm_dashboard')

    return render(request, 'core/confirm_delete.html', {'internship': internship})

@login_required
def view_applicants(request, internship_id):
    internship = get_object_or_404(Internship, id=internship_id)
    applicants = InternshipApplication.objects.filter(internship=internship)

    return render(request, 'core/view_applicants.html', {
        'internship': internship,
        'applicants': applicants
    })
@login_required
def approve_project(request, project_id):
    project = get_object_or_404(HouseProject, id=project_id)

    if request.method == "POST":
        firm = get_object_or_404(Firm, user=request.user)
        message = request.POST.get('approval_message')

        project.status = 'approved'
        project.firm = firm
        project.approval_message = message
        project.firm_response = message  # ✅ This line must be present
        project.save()

        messages.success(request, "Project approved.")
    return redirect('firm_dashboard')


def client_dashboard(request):
    from .forms import HouseProjectForm

    if request.method == 'POST':
        form = HouseProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user
            project.save()
            messages.success(request, "✅ House project submitted successfully!")
            return redirect('client_dashboard')  # this ensures page reload + message
        else:
            messages.error(request, "⚠️ Please correct the errors in the form.")
    else:
        form = HouseProjectForm()

    firms = User.objects.filter(userprofile__role='firm')
    house_projects = HouseProject.objects.filter(client=request.user)

    return render(request, 'core/client_dashboard.html', {
        'form': form,
        'firms': firms,
        'house_projects': house_projects,
    })

@login_required
def internships_list(request):
    internships = Internship.objects.all()
    return render(request, 'core/internships_list.html', {'internships': internships})

@login_required
def internship_detail(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    return render(request, 'core/internship_detail.html', {'internship': internship})

def test_template(request):
    return render(request, 'core/test_template.html')
# core/views.py
from django.shortcuts import render, get_object_or_404
from .models import Firm

# in views.py
@login_required
def firm_profile(request, firm_id):
    firm = get_object_or_404(Firm, id=firm_id)
    return render(request, 'core/firm_profile.html', {'firm': firm})



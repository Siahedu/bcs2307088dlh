
from django.shortcuts import render, redirect 
from django.contrib import messages
from .models import Student, Meetup, Staff, Registration
from django.db.models import Q
# Create your views here.
from django.db.models import Q
from django.shortcuts import render
from .models import Meetup
from .models import Meetup, Comment, Student, Registration

def home(request):
    # Get all meetups to display initially
    displaydata = Meetup.objects.all()

    # Check for search query in the GET request
    query = request.GET.get('search')
    if query:
        # Perform search using icontains for partial and case-insensitive matches
        findmeetup = Meetup.objects.filter(
            Q(meetup_name__icontains=query) | Q(meetup_description__icontains=query ))
        
    else:
        findmeetup = Meetup.objects.none()  # Return an empty queryset if no search query

    # Combine all necessary data into one context dictionary
    context = {
        'displaydata': displaydata,
        'findmeetup': findmeetup,
    }

    return render(request, "home.html", context)




def join(request):
    profile1 = Student.objects.all().values()  
   
    if request.method == 'POST':
        student_id = request.POST['student_id']
        student_email = request.POST['student_email']
        student_password = request.POST['student_password']
        student_phone = request.POST['student_phone']
        # For file upload, you need to get the file from request.FILES
        #profile_picture = request.FILES.get('profile_picture') 
      


        # Create the new Student object
        data = Student(
            student_id=student_id,
            student_email=student_email,
            student_password=student_password,
            student_phone=student_phone,
            #profile_picture=profile_picture,
         
        )
        data.save()

        context = {
            'studentmentorid': profile1,  
            
            'message': ' YOUR ACCOUNT HAS BEEN SAVED'  
        }

        return render(request, "join.html", context)
    else:
        context = {
            'studentmentor': profile1, 
            'message': '',
        }

    return render(request, 'join.html', context)



def login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('student_password')
        role = request.POST.get('role')  # Get the selected role

        if role == 'student':
            try:
                # Try to get a student with the provided student_id
                student = Student.objects.get(student_id=student_id)

                # Check if the provided password matches the one in the database
                if student.student_password == password:
                    # Store the student's ID in the session
                    request.session['student_id'] = student.student_id
                    messages.success(request, 'Login successful!')
                    return redirect('home')  # Redirect to homepage
                else:
                    messages.error(request, 'Invalid password.')
                    return redirect('login')

            except Student.DoesNotExist:
                messages.error(request, 'Student does not exist.')
                return redirect('login')

        elif role == 'staff':
            try:
                # Try to get a staff with the provided staff_id
                staff = Staff.objects.get(staff_id=student_id)

                # Check if the provided password matches
                if staff.staff_password == password:
                    # Store the staff's ID in the session
                    request.session['staff_id'] = staff.staff_id
                    messages.success(request, 'Login successful!')
                    return redirect('manage_meetup')  # Redirect to staff's homepage
                else:
                    messages.error(request, 'Invalid password.')
                    return redirect('login')

            except Staff.DoesNotExist:
                messages.error(request, 'Staff does not exist.')
                return redirect('login')

    return render(request, 'login.html')


from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, get_object_or_404, redirect


def meetup_detail(request, meetup_id):
    meetup = get_object_or_404(Meetup, meetup_id=meetup_id)
    comments = Comment.objects.filter(meetup=meetup)
    
    # Get the current logged-in student from the session
    current_student_id = request.session.get('student_id')
    
    if current_student_id:
        # Retrieve the student object using the student ID from session
        current_student = get_object_or_404(Student, student_id=current_student_id)
    else:
        messages.error(request, "You must be logged in to register or comment.")
        return redirect('login')  # Redirect to login if not logged in

    if request.method == "POST":
        # Handle registration
        if "register_meetup" in request.POST:
            if not Registration.objects.filter(meetup=meetup, student=current_student).exists():
                Registration.objects.create(meetup=meetup, student=current_student)
                messages.success(request, "You have successfully registered for the meetup!")
            else:
                messages.error(request, "You are already registered for this meetup.")

        # Handle comments
        elif "submit_comment" in request.POST:
            comment_text = request.POST.get("comment_text")
            if comment_text:
                Comment.objects.create(student=current_student, meetup=meetup, comment_text=comment_text)
                messages.success(request, "Your comment has been posted!")
            else:
                messages.error(request, "Please provide a comment.")

        # Handle comment deletion
        elif "delete_comment" in request.POST:
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, comment_id=comment_id)

            # Ensure only the logged-in student can delete their own comment
            if comment.student.student_id == current_student.student_id:
                comment.delete()
                messages.success(request, "Comment deleted successfully.")
            else:
                messages.error(request, "You can only delete your own comments.")

        return redirect('meetup_detail', meetup_id=meetup_id)

    context = {
        'meetup': meetup,
        'comments': comments,
        'current_student_id': current_student_id,  # Pass the current student ID to the template
    }
    return render(request, 'meetup_detail.html', context)

def manage_meetup(request):
    # Fetch all meetups with related registrations
    meetups = Meetup.objects.all()
    context = {
        'meetups': meetups,
    }
    return render(request, 'manage_meetup.html', context)

def add_meetup(request):
    if request.method == 'POST':
        meetup_name = request.POST['meetup_name']
        meetup_description = request.POST['meetup_description']
        meetup_date = request.POST['meetup_date']
        meetup_location = request.POST['meetup_location']
        meetup_poster = request.FILES.get('meetup_poster')

        new_meetup = Meetup(
            meetup_name=meetup_name,
            meetup_description=meetup_description,
            meetup_date=meetup_date,
            meetup_location=meetup_location,
            meetup_poster=meetup_poster
        )
        new_meetup.save()

        messages.success(request, "Meetup added successfully!")
        return redirect('manage_meetup')

    return render(request, 'add_meetup.html')

def update_meetup(request, meetup_id):
    meetup = get_object_or_404(Meetup, meetup_id=meetup_id)

    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        meetup.meetup_name = request.POST['meetup_name']
        meetup.meetup_description = request.POST['meetup_description']
        meetup.meetup_date = request.POST['meetup_date']
        meetup.meetup_location = request.POST['meetup_location']
        meetup.meetup_poster = request.FILES.get('meetup_poster', meetup.meetup_poster)

        meetup.save()
        messages.success(request, "Meetup updated successfully!")
        return redirect('manage_meetup')

    context = {'meetup': meetup}
    return render(request, 'update_meetup.html', context)

def delete_meetup(request, meetup_id):
    meetup = get_object_or_404(Meetup, meetup_id=meetup_id)
    meetup.delete()
    messages.success(request, "Meetup deleted successfully!")
    return redirect('manage_meetup')

from django.http import HttpResponseNotAllowed

def approve_registration(request, registration_id):
    registration = get_object_or_404(Registration, pk=registration_id)
    
    # Check if request is POST and has _method as PUT
    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        registration.status = 'approved'
        registration.save()
        messages.success(request, 'Student registration has been approved.')
        return redirect('manage_meetup')  # Redirect back to the meetups management page
     
    return HttpResponseNotAllowed(['POST'])


def reject_registration(request, registration_id):
    registration = get_object_or_404(Registration, pk=registration_id)
    
    # Check if request is POST and has _method as PUT
    if request.method == 'POST' and request.POST.get('_method') == 'PUT':
        registration.status = 'rejected'
        registration.save()
        messages.success(request, 'Student registration has been rejected.')
        return redirect('manage_meetup')  # Redirect back to the meetups management page
    
    return HttpResponseNotAllowed(['POST'])



def student_profile(request):
    # Retrieve current student ID from the session
    student_id = request.session.get('student_id')
    
    if student_id:
        # Get the student instance
        student = Student.objects.get(student_id=student_id)
        
        # Fetch all the meetups the student has registered for
        registrations = Registration.objects.filter(student=student)

        # Pass the registrations to the template
        context = {
            'student': student,
            'registrations': registrations,
        }
        return render(request, 'student_profile.html', context)
    
    # Redirect to login if not authenticated
    return redirect('login')



from django.shortcuts import redirect
from django.contrib import messages

def logout(request):
    # Clear the session and log the user out
    request.session.flush()  # Removes all session data
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')  # Redirect to the login page




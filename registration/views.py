from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from .forms import UserProfileForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from pdfminer.high_level import extract_text
import os
import re

def extract_resume_data(resume_path):
    text = extract_text(resume_path)
    data = {}

    # Extract name (assuming the first line is the name)
    lines = text.split('\n')
    if lines:
        data['name'] = lines[0]

    # Extract email
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    email_match = re.search(email_pattern, text)
    if email_match:
        data['email'] = email_match.group(0)

    # Extract phone number (simple pattern)
    phone_pattern = r'\+?\d[\d -]{8,12}\d'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        data['phone'] = phone_match.group(0)

    # Extract address (assuming address is between certain keywords)
    address_pattern = r'Address:\s*(.*?)\n'
    address_match = re.search(address_pattern, text)
    if address_match:
        data['address'] = address_match.group(1)

    return data

def home(request):
    if request.method == 'POST' and 'resume' in request.FILES:
        resume = request.FILES['resume']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
        filename = fs.save(resume.name, resume)
        resume_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename)
        request.session['resume_path'] = resume_path

        return redirect('form')

    form = UserProfileForm()
    return render(request, 'upload.html', {'form': form})

def form_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UserProfileForm()

        # Prefill form with parsed data from the resume
        resume_path = request.session.get('resume_path')
        if resume_path:
            data = extract_resume_data(resume_path)
            initial_data = {
                'first_name': data.get('name', '').split()[0],
                'last_name': ' '.join(data.get('name', '').split()[1:]),
                'email': data.get('email', ''),
                'phone_number': data.get('phone', ''),
                'address': data.get('address', '')
            }
            form = UserProfileForm(initial=initial_data)

    return render(request, 'filledForm.html', {'form': form})

def parse_resume(request):
    if request.method == 'POST' and 'resume' in request.FILES:
        resume = request.FILES['resume']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
        filename = fs.save(resume.name, resume)
        resume_path = os.path.join(settings.MEDIA_ROOT, 'temp', filename)

        try:
            data = extract_resume_data(resume_path)
            return JsonResponse(data)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
    return HttpResponseBadRequest("Invalid request")

def success(request):
    return render(request, 'success.html')

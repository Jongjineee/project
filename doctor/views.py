from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import Category, Doctor, Profile
from .forms import SignupForm, DoctorForm, LoginForm, EnterpriseForm, EditProfileForm
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as django_logout
from django.contrib import messages
from django.template import RequestContext
###############################################

# Create your views here.

#################################################
def form_test(request):

	return render(request, 'doctor/doctor_Account.html')


def index(request):
	user=request.user
	categories = Category.objects.filter(sort="DOCTOR")
	context = {'categories': categories, 'user': user}
	return render(request, 'doctor/index.html', context)


def profile(request, pk):
	user = User.objects.get(pk=pk)
	categories = Category.objects.filter(sort="DOCTOR")
	profile = Profile.objects.filter(user=user)
	user = request.user
	context = {'user': user, 'profile': profile, 'categories': categories}
	return render(request, 'doctor/doctor_Account.html', context)


def profile_edit(request, pk):
	instance = get_object_or_404(Profile, user=request.user)
	categories = Category.objects.filter(sort="DOCTOR")
	user = request.user

	if request.method == "POST":
		form = EditProfileForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form = form.save(commit=False)
			form.user = request.user
			form.save()
			return redirect('doctor:profile', pk)
	else:
		form = EditProfileForm()
	return render(request, 'doctor/edit_profile.html', {'form': form, 'categories': categories, 'user': user})


def signup(request):
	categories = Category.objects.filter(sort="DOCTOR")
	user = request.user
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			new_user = authenticate(username=form.cleaned_data['username'],
									password=form.cleaned_data['password1'],
									)
			login(request, new_user)
			return redirect(settings.LOGIN_REDIRECT_URL)
	else:
		form = SignupForm()
	return render(request, 'account/signup.html', {
		'form': form,
		'categories': categories,
		'user': user
	})


def signin(request):
	if request.method == "POST":
		form = LoginForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('doctor:index')
		else:
			return HttpResponse('로그인 실패. 다시 시도 해보세요.')
	else:
		form = LoginForm()
		return render(request, 'account/login.html', {'form': form})


def logout(request):
	django_logout(request)
	return render(request, 'doctor/index.html')


def doctor_certification(request, pk):
	user = User.objects.get(pk=pk)
	category = Category.objects.filter(sort='DOCTOR')
	for i in category:
		if user == i.user:
			messages.error(request, '이미 등록!', extra_tags='alert')
			return redirect('doctor:index')
	if request.method == 'POST':
		form = DoctorForm(request.POST, request.FILES)
		if form.is_valid():
			form = form.save(commit=False)
			form.user = user
			# Category 저장

			form.save()
			Category.objects.create(user=user, sort='DOCTOR')
			return redirect('doctor:index')
	else:
		form = DoctorForm()
	return render(request, 'doctor/doctor_certification.html', {
		'form': form,
	})


def enterprise_certification(request, pk):
	user = User.objects.get(pk=pk)
	category = Category.objects.filter(sort='ENTERPRISE')

	if request.method == 'POST':
		form = EnterpriseForm(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.user = user

			# Category 저장
			for i in category:
				if user == i.user:
					messages.warning(request, '이미 등록')
					return redirect('doctor:index')
			form.save()
			Category.objects.create(user=user, sort='ENTERPRISE')
			messages.success(request, '등록 완료')
			return redirect('doctor:index')
	else:
		form = EnterpriseForm()
	return render(request, 'doctor/enterprise_certification.html', {
		'form': form,
	})

def doctor_form(request, pk):
	user = request.user
	categories = Category.objects.filter(sort="DOCTOR")
	doctor_info = Doctor.objects.get(user=user)
	context = {
		'id': user.username,
		'doctorName': doctor_info.name,
		'medicalName': doctor_info.medical_name,
		'address': doctor_info.address,
		'phoneNumber': doctor_info.phone_number,
		'licenseNumber': doctor_info.license_number,
		'categories': categories
	}
	return render(request, 'doctor/doctor_form.html', context)


































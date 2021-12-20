from recolor.tools1 import Core1
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .tools import Core
from PIL import Image
import numpy as np
import base64
import io
import cv2

# home page function here
def home(request):
    return render(request, 'home.html')

#re.search ('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
# this is the function to render the signup template
def signup(request):
    if request.method == 'POST':
        if request.POST['email']:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.get(username=request.POST['email'])
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        request.POST['email'],
                        password=request.POST['password1'],
                    )
                    auth.login(request, user)
                    return redirect('upload')
            else:
                return render(request, 'signup.html', {'err': 'Mismatched password'})
        else:
            return render(request, 'signup.html', {'err': 'Invalid Email'})
    return render(request, 'signup.html')


# function for login
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(
            username=request.POST['email'],
            password=request.POST['password']
        )
        if user is not None:
            # print('#' * 150)
            # print(user.username, '|', user.is_superuser, '|', user.groups)
            # print('#' * 150)

            # for admin logic
            if user.is_superuser:
                auth.login(request, user)
                return redirect('option')

            auth.login(request, user)
            return redirect('option')
    else:
        return render(request, 'login.html')


# logout function
@login_required(login_url='/login/')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')


def numpy_encoded(array):
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(array)
    buff = io.BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode('utf-8')



@login_required(login_url='/login/')
def option(request):
    return render(request, 'option.html')



# this function will be the actual backbone and the
# logic of the code
@login_required(login_url='/login/')
def upload(request):
    if request.method == 'POST':
        image = request.FILES['file-upload-field']
        # print(type(image))
        #input validation
        if image.name.split('.')[-1] in ['jpg', 'jpeg', 'png']:
            encoded = base64.b64encode(image.file.read()).decode('utf-8')
            mime = "image/jpeg"
            uri = "data:%s;base64,%s" % (mime, encoded)

            decoded = base64.b64decode(encoded)
            image_ = Image.open(io.BytesIO(decoded))
            image_np = np.array(image_)
            core = Core(image_np)

            print('#' * 150)
            core.simulate()
            core.correct()
            core.simulate(simulated_recolored=True)
            enc_simulated = "data:%s;base64,%s" % (mime, numpy_encoded(core.simulated_image))
            print('\n Simulation done')
            enc_recolored = "data:%s;base64,%s" % (mime, numpy_encoded(core.recolored))
            print('\n Recoloring done')
            enc_sim_recolored = "data:%s;base64,%s" % (mime, numpy_encoded(core.simulated_recolored_image))
            print('\n Simulating Recolored done\n')

            # actual conversion logic will happen here
            context = {
                'image': uri,
                'recolored': enc_recolored,
                'simulated': enc_simulated,
                'simulated_recolored': enc_sim_recolored
            }
            return render(request, 'upload.html', context)
        else:
            print("invalid format")
            return render(request, 'upload.html', {'msg': f'File format {image.name} is invalid'})
        # print(image)
    return render(request, 'upload.html')


@login_required(login_url='/login/')
def upload1(request):
    if request.method == 'POST':
        image = request.FILES['file-upload-field']
        # print(type(image))
        #input validation
        if image.name.split('.')[-1] in ['jpg', 'jpeg', 'png']:
            encoded = base64.b64encode(image.file.read()).decode('utf-8')
            mime = "image/jpeg"
            uri = "data:%s;base64,%s" % (mime, encoded)

            decoded = base64.b64decode(encoded)
            image_ = Image.open(io.BytesIO(decoded))
            image_np = np.array(image_)
            core1 = Core1(image_np)

            print('#' * 150)
            core1.simulate()
            core1.correct()
            core1.simulate(simulated_recolored=True)
            enc_simulated1 = "data:%s;base64,%s" % (mime, numpy_encoded(core1.simulated_image))
            print('\n Simulation done')
            enc_recolored1 = "data:%s;base64,%s" % (mime, numpy_encoded(core1.recolored))
            print('\n Recoloring done')
            enc_sim_recolored1 = "data:%s;base64,%s" % (mime, numpy_encoded(core1.simulated_recolored_image))
            print('\n Simulating Recolored done\n')

            # actual conversion logic will happen here
            context = {
                'image': uri,
                'recolored': enc_recolored1,
                'simulated': enc_simulated1,
                'simulated_recolored': enc_sim_recolored1
            }
            return render(request, 'upload.html', context)
        else:
            print("invalid format")
            return render(request, 'upload1.html', {'msg': f'File format {image.name} is invalid'})
        # print(image)
    return render(request, 'upload1.html')

@login_required(login_url='/login/')
def admin(request):
    return render(request, 'admin.html')

@login_required(login_url='/login/')
def admin1(request):
    return render(request, 'admin1.html')

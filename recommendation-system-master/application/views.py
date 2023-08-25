from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
import os

def get_bs4_version(fig_object):
    import io, base64
    flike = io.BytesIO()
    fig_object.savefig(flike)
    b64 = base64.b64encode(flike.getvalue()).decode()
    return b64


def admin_portal(request):
    if request.user.is_authenticated and request.user.is_superuser:
        my_graph_list = get_accuracy()
        context = {
            'graph_list': my_graph_list,
            'registered_users': User.objects.all().count() - 1,
            'visits': Visit.objects.all().count()
        }
        return render(request, "admin.html", context)

    return redirect("index")


def calculate_response(answers_array):
    base_dir = settings.BASE_DIR
    csv_path = os.path.join(base_dir, "static", "society_root.csv")

    # package for data analysis
    import pandas as pd

    #import Decision Tree Classifier model
    from sklearn .tree import DecisionTreeClassifier

    # to ignore warnings
    import warnings
    warnings.filterwarnings('ignore')

    #--------reading the .csv file as input------------#
    society_data = pd.read_csv(csv_path)

    #Spliting the input and output from the dataset

    #input columns
    X = society_data.drop(columns=['Suggestion'])

    #output column
    Y = society_data['Suggestion']

    #------------------Training and testing with Decision Tree----------------#
    model = DecisionTreeClassifier()
    model.fit(X, Y)

    #There are 12 input columns and one output column in the dataset
    #'0' means 'No'
    #'1' means 'Yes'
    #For predictions

    predictions = model.predict([answers_array])
    return predictions.tolist()[0].split(",")

def reGenerate(output):
    my_list = []
    for x in output:
        x = x.strip()
        if x == "IUCCS":
            my_list.append([
                "Iqra University Climate Change Society",
                "https://www.facebook.com/IUCCS.khi"
            ])
        elif x == "IUDLS":
            my_list.append([
                "Iqra University Debates and Literary Society",
                "https://www.facebook.com/IUDLS"
            ])
        elif x == "IUDS":
            my_list.append([
                "IU Dramatics Society",
                "https://www.facebook.com/IUDSociety"
            ])
        elif x == "IUES":
            my_list.append([
                "IU Entrepreneurship Society",
                "https://www.facebook.com/IUESOFFICIAL"
            ])
        elif x == "IUEventSociety":
            my_list.append([
                "Iqra University Events Society",
                "https://www.facebook.com/IUEventSociety"
            ])
        elif x == "IUGRS":
            my_list.append([
                "Iqra University Gaming and Robotics Society",
                "https://www.facebook.com/IUGamingAndRoboticsSociety"
            ])
        elif x == "IUCSR":
            my_list.append([
                "Iqra University Corporate Social Responsibility",
                "https://www.facebook.com/IUCSR.khi"
            ])
        elif x == "IUPS":
            my_list.append([
                "IU Photography Society",
                "https://www.facebook.com/iuphotographysociety"
            ])
        elif x == "IUSS":
            my_list.append([
                "Iqra University Sports Society",
                "https://www.facebook.com/IUSports"
            ])
        else:
            my_list.append([
                "Your interests haven't met any society please try again!",
                "http://127.0.0.1:8000/society/"
            ])
    
    return my_list

def submit_response(request):
    
    output = {
        'status': False,
        'message': None
    }

    if request.method == "GET":
        response = request.GET.get("response")
        if response:
            response = json.loads(response)

            if request.user.is_authenticated:
                new_response = UserResponse(user = request.user)
            else:
                new_response = UserResponse()
          
            new_response.save()

            answers_array = []
            
            for i in response:
                question_id = i['question']
                answer_id = i['answer']

                question = Question.objects.get(id = question_id)
                answer = Answer.objects.get(id = answer_id)

                new_response.question_answers.create(
                    question = question,
                    answer = answer
                )

                answers_array.append(answer.boolean)

            model_output = calculate_response(answers_array)
            output['response'] = reGenerate(model_output)
            output['status'] = True
        return JsonResponse(output)

def index(request):
    Visit.objects.create()
    # return render(request, "signin.html")
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("admin-portal")

    elif request.user.is_authenticated:
        return redirect("society")

    return render(request, 'index.html')


@login_required
def society(request):
    all_questions = Question.objects.all()
    context = {
        'all_questions': all_questions,
        'total_questions': all_questions.count()
    }
    return render(request, 'society.html', context)


# function for signup

def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
        
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            messages.success(request, "Your account has been created!")
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)
 
    return render(request, "signup.html")


# function for login

def login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        NEXT = request.POST.get("next")
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            if NEXT:
                return redirect(NEXT)
            else:
                return redirect("index")
        else:
            messages.error(request, "Incorrect login details!")
            return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")

@login_required
def department(request):
    all_questions = Dept_Question.objects.all()
    context = {
        'all_questions': all_questions,
        'total_questions': all_questions.count()
    }
    return render(request, 'department.html', context)

def department_result(request):
    return render(request, 'department_result.html')

def dept_calculate_response(answers_array):
    base_dir = settings.BASE_DIR
    csv_path = os.path.join(base_dir, "static", "Department_root.csv")
  
    # package for data analysis
    import pandas as pd

    #import NearestCentroid model
    from sklearn.neighbors import NearestCentroid

    # to ignore warnings
    import warnings
    warnings.filterwarnings('ignore')

    #--------reading the .csv file as input------------#
    department_data = pd.read_csv(csv_path)

    #Spliting the input and output from the dataset

    #input columns
    X = department_data.drop(columns=['Suggestion'])

    #output column
    Y = department_data['Suggestion']

    #input columns
    X = department_data.drop(columns=['Suggestion'])

    #output column
    Y = department_data['Suggestion']

    #------------------Training and testing with XGBClassifier----------------#
    model = NearestCentroid()
    model.fit(X, Y)

    #------------------Getting prediction----------------#
    predictions = model.predict([answers_array])
    return predictions.tolist()[0].split(",")


def dept_submit_response(request):
    
    output = {
        'status': False,
        'message': None
    }

    if request.method == "GET":
        response = request.GET.get("response")
        if response:
            response = json.loads(response)

            if request.user.is_authenticated:
                new_response = Dept_UserResponse(user = request.user)
            else:
                new_response = Dept_UserResponse()

            new_response.save()

            answers_array = []
            
            for i in response:
                question_id = i['question']
                answer_id = i['answer']

                question = Dept_Question.objects.get(id = question_id)
                answer = Dept_Answer.objects.get(id = answer_id)

                new_response.question_answers.create(
                    question = question,
                    answer = answer
                )

                answers_array.append(answer.boolean)

            new_response.save()
            print(answers_array)
            model_output = dept_calculate_response(answers_array)
            output['response'] = model_output

            output['status'] = True

    return JsonResponse(output)


def get_accuracy():
    # import packages
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler 
    from sklearn.neighbors import NearestCentroid
    from sklearn.linear_model import LogisticRegression
    import matplotlib.pyplot as plt
    from sklearn.metrics import plot_confusion_matrix
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    import pandas as pd
    import io, base64

    base_dir = settings.BASE_DIR
    csv_path = os.path.join(base_dir, "static", "Department_root.csv")

    # import dataset
    department_data = pd.read_csv(csv_path)

    # Spliting the input and output from the dataset
    # input columns
    X = department_data.drop(columns=['Suggestion'])
    # output column
    y = department_data['Suggestion']


    # split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10,random_state=0)


    # Standardize the data set
    SC_X=StandardScaler()
    X_train_Scaled=SC_X.fit_transform(X_train)
    X_test=Scaled=SC_X.transform(X_test)


    # Select ML classifiers
    classifiers=[ NearestCentroid(),LogisticRegression(solver="liblinear",max_iter=100)]

    graph_list = []
    # Print the confusion matrix using Matplotlib
    for clf in classifiers:
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        fig1, ax = plt.subplots(figsize=(15, 10))
        fig=plot_confusion_matrix(clf, X_test, y_test, display_labels=["Business Studies","Computer Sciences","Engineering Studies","Fashion Design","Media Studies"], ax=ax)
        fig.figure_.suptitle("Confusion Matrix for  " + str(clf))
        bs4 = get_bs4_version(fig1)

        my_obj = {
            'img': bs4,
            'params': [
                {
                    'name': 'Precision',
                    'value': precision_score(y_test, y_pred, average='macro')
                },
                {
                    'name': 'Recall',
                    'value': recall_score(y_test, y_pred, average='macro')
                },
                {
                    'name': 'Accuracy',
                    'value': accuracy_score(y_test, y_pred)
                },
                {
                    'name': 'F1 Score',
                    'value': f1_score(y_test, y_pred, average='macro')
                },
            ]
        }

        graph_list.append(my_obj)
    
    return graph_list
                
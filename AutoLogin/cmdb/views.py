from django.shortcuts import render

# Create your views here.
from worm.AutoLogin import main


def index(resquest):
    return render(resquest,"index.html")

def Login_Auto(resquest):
    main()
    return render(resquest,"index.html")
from django.urls import path
import app.views as views

urlpatterns = [
    path("number/generate/", views.GenerateNumberView.as_view(), name = "number-generate"),
    path("number/", views.NumberView.as_view(), name = "number"),
    path("doings/", views.CheckList.as_view(), name = "doings"),
    path("wheel/", views.Wheel.as_view(), name = "wheel"),
    path("ask/", views.Ask.as_view(), name = "doings"),
    path("password/", views.Password.as_view(), name = "password"),
    path("password/generate/", views.PasswordGenerateView.as_view(), name = "password-generate"),
    path("ask/generate/", views.AskGenerate.as_view(), name = "doings-generate"),
    path("ask/last/", views.AskLast.as_view(), name = "doings-last"),
    path("account/signin/", views.SigninView.as_view(), name = "account-sigin"),
    path("account/signup/", views.SignupView.as_view(), name = "account-signup"),
    path("winvk/", views.WinVK.as_view(), name = "winvk"),
    path("wintg/", views.WinTG.as_view(), name = "wintg"),
    path("winig/", views.WinIG.as_view(), name = "winig"),

    path("question/", views.Question.as_view(), name = "question"),
    path("question/generate/", views.QuestionGenerate.as_view(), name = "question-generate"),
    path("question/answer/", views.AnswerView.as_view(), name = "question-answer"),

    path("saying/", views.Saying.as_view(), name = "saying"),
    path("saying/generate/", views.SayingGenerateView.as_view(), name="saying-generate"),
    path("saying/vote/", views.SayingVoteView.as_view(), name="saying-vote"),
    path("saying/fav/", views.SayingFavView.as_view(), name="saying-fav"),

    path("ticket/", views.Ticket.as_view(), name = "ticket"),
    path('ticket/generate/', views.TicketGenerateView.as_view(), name='ticket-generate'),
    
    path("fact/", views.Fact.as_view(), name = "fact"),
    path("fact/generate/", views.FactGenerateView.as_view(), name="fact-generate"),
    path("fact/vote/", views.FactVoteView.as_view(), name="fact-vote"),
    path("fact/fav/", views.FactFavVIew.as_view(), name="fact-fav"),

    path("", views.IndexView.as_view(), name = "index")
    
]

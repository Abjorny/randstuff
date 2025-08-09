from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import QuestionModel, TicketStat, AskModel, FactModel, SayingModel, Number
import app.serializers as serializers
from django.db.models import Q
import random
import string

class IndexView(APIView):
    def get(sefl, request):
        return render(request, "index.html")

class FactFavVIew(APIView):
    def get(self, request):
        fact = FactModel.objects.order_by("-likes").first()
        return render(request, "fact_fav.html", {"fact": fact})

class FactGenerateView(APIView):
    def post(self, request):
        fact = FactModel.objects.order_by("?").first() 
        data = serializers.FactSerializer(fact).data
        return Response({"fact": data})

class SayingFavView(APIView):
    def get(self, request):
        saying = SayingModel.objects.order_by("-likes").first()
        return render(request, "saying_fav.html", {"saying": saying})

class SayingGenerateView(APIView):
    def post(self, request):
        saying = SayingModel.objects.order_by("?").first() 
        data = serializers.SayingSerializer(saying).data
        return Response({"saying": data})

class SayingVoteView(APIView):
    def post(self, request):
        saying_id = request.data.get("id")
        rate = request.data.get("rate")

        saying = SayingModel.objects.get(id=saying_id)

        if rate == "like":
            saying.likes += 1
        else:
            saying.dislikes += 1

        saying.save()
        return Response({"ok": True})

class FactVoteView(APIView):
    def post(self, request):
        fact_id = request.data.get("id")
        rate = request.data.get("rate")

        fact = FactModel.objects.get(id=fact_id)

        if rate == "like":
            fact.likes += 1
        else:
            fact.dislikes += 1

        fact.save()
        return Response({"ok": True})

class TicketGenerateView(APIView):
    def post(self, request):
        ticket_number = f"{random.randint(0, 999999):06d}"

        lucky = random.choice([True, False])

        stat_obj, created = TicketStat.objects.get_or_create(id=1)

        # Обновляем статистику
        stat_obj.count += 1
        if lucky:
            stat_obj.lucky += 1
        stat_obj.save()

        response_data = {
            "ticket": ticket_number,
            "lucky": lucky,
            "stat": {
                "count": str(stat_obj.count),
                "lucky": str(stat_obj.lucky),
            }
        }

        return Response(response_data)

class AnswerView(APIView):
    def post(self, request):
        question_id = request.data.get("id")
        selected_number = request.data.get("number")

        question = QuestionModel.objects.get(id=question_id)

        selected_number_int = int(selected_number)

        correct_answer = question.correct_answer

        stat = request.session.get('answer_stat', {"total": 0, "correct": 0, "incorrect": 0})

        # Обновляем статистику
        stat["total"] += 1
        if selected_number_int == correct_answer:
            stat["correct"] += 1
            success = True
        else:
            stat["incorrect"] += 1
            success = False

        request.session['answer_stat'] = stat

        return Response({
            "answer" : {
                "success": success,
                "correct": str(correct_answer),
            },
            "stat": stat
        })

class Question(APIView):
    def get(self, request):
        return render(request, "question.html")

class QuestionGenerate(APIView):
    def post(self, request):
        objects = QuestionModel.objects.all()
        serializer = serializers.QuestionSerializer(objects, many=True)
        choice = random.choice(serializer.data)  
        return Response({"question": choice})

class Saying(APIView):
    def get(self, request):
        return render(request, "saying.html")

class Ticket(APIView):
    def get(sefl, request):
        return render(request, "ticket.html")

class Fact(APIView):
    def get(self, request):
        return render(request, "fact.html")

class WinVK(APIView):
    def get(self, request):
        return render(request, "win/winvk.html")

class WinTG(APIView):
    def get(self, request):
        return render(request, "win/wintg.html")

class WinIG(APIView):
    def get(self, request):
        return render(request, "win/winig.html")
        
class SignupView(APIView):
    def get(self, request):
        return render(request, "authorise/signup.html")

class SigninView(APIView):
    def get(self, request):
        return render(request, "authorise/signin.html")

class PasswordGenerateView(APIView):
    def post(self, request):
            length = int(request.data.get("length", 8))
            use_numbers = request.data.get("numbers", "0") == "1"
            use_symbols = request.data.get("symbols", "0") == "1"

            chars = list(string.ascii_letters)

            if use_numbers:
                chars += list(string.digits)

            if use_symbols:
                chars += list("!@#$%^&*()_+-=[]{}|;:,.<>?")

            password = ''.join(random.choice(chars) for _ in range(length))

            return Response({"password": password})

class Password(APIView):
    def get(self, request):
            length = 8
            use_numbers = 0
            use_symbols =0

            chars = list(string.ascii_letters)

            if use_numbers:
                chars += list(string.digits)

            if use_symbols:
                chars += list("!@#$%^&*()_+-=[]{}|;:,.<>?")

            password = ''.join(random.choice(chars) for _ in range(length))
            return render(request, "password.html", {"password" : password})

class Wheel(APIView):
    def get(self, request):
        return render(request, "wheel.html")

class AskLast(APIView):
    def post(self, request):
        objects = AskModel.objects.all()
        serializer = serializers.AskSerializer(objects, many=True)
        return Response({"last" : serializer.data[::-1]}) 

class AskGenerate(APIView):
    def post(self, request):
        predictions = ["Никаких<br>сомнений", "Пока не ясно,<br>попробуй<br>снова",  "Мой ответ<br>нет", "Весьма<br>спорно", "Мне кажется<br>да", "Мой ответ<br>нет", "Сейчас нельзя<br>предсказать", "По моим<br>данным<br>нет",  "Пока не ясно,<br>попробуй<br>снова",  "Даже не<br>думай" ]
        question = request.data.get("question", "")
        prediction = random.choice(predictions)
        if question and prediction:
            if AskModel.objects.count() >= 5:
                oldest = AskModel.objects.earliest('created_at')  
                oldest.delete()
            prediction = prediction.replace("<br>", " ")
            AskModel.objects.create(question=question, prediction=prediction)
        return Response({ "ask" : {"question" : question, "prediction" : prediction }})

class Ask(APIView):
    def get(self, request):
        return render(request, "ask.html")

class NumberView(APIView):
    def get(self, request):
        value = random.randint(1, 100)
        return render(request, "number.html", { "number" : value}) 

class CheckList(APIView):
    def get(self, request):
        return render(request, "checkList.html")

class GenerateNumberView(APIView):
    def post(self, request):
        result = {"number": []}

        count = int(request.data.get("count", 1))
        from_value = request.data.get("from", "range")

        start = int(request.data.get("start", 0))
        end = int(request.data.get("end", 100))

        list_numbers = request.data.get("list", [])
        if list_numbers:
            list_numbers = list_numbers.split("\n")

        unique = int(request.data.get("unique", 0))
        exclude_list = request.data.get("exclude_list", [])
        if exclude_list:
            exclude_list = exclude_list.split("\n")

        exclude_list = list(map(int, exclude_list))
        list_numbers = list(map(int, list_numbers)) if list_numbers else []

        # Формируем доступные числа
        if from_value == "range":
            available = list(range(start, end + 1))
        elif from_value == "list":
            available = list_numbers
        else:
            return Response({"error": True})

        available = [num for num in available if num not in exclude_list]

        # Числа из админки (не использованные, в диапазоне/списке, по порядку)
        numbers_from_admin = Number.objects.filter(
            value__in=available,
            used=False
        ).order_by("order")[:count]

        admin_values = [n.value for n in numbers_from_admin]
        result["number"].extend(admin_values)

        # Помечаем их как использованные
        Number.objects.filter(id__in=[n.id for n in numbers_from_admin]).update(used=True)

        # Если нужно добрать недостающее количество
        remaining_count = count - len(admin_values)
        if remaining_count > 0:
            available = [num for num in available if num not in admin_values]

            if unique:
                available = list(set(available))
                if remaining_count > len(available):
                    result["number"].extend(available)
                else:
                    result["number"].extend(random.sample(available, remaining_count))
            else:
                if not available:
                    return Response({"error": True})
                result["number"].extend(random.choice(available) for _ in range(remaining_count))

        return Response(result)

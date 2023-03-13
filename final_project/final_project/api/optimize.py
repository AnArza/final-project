from game.models import History, Config
from .helper_functions import *
from django.db.models import Q


def betting_limit(budget, prob):
    # answer = float()
    histories = History.objects.all()
    if len(histories) == 1:
        history = History.objects.latest('id')
        # print(history)
        history.current_round = 1
    else:
        history = History.objects.latest('id')
        history.current_round = History.objects.filter(~Q(id=history.id)).reverse().first().current_round + 1
        print(History.objects.filter(id=history.id).reverse().first().id)
    history.save()
    rest_rounds = Config.get_solo().impressions_total - history.current_round + 1
    budget_for_round = float(budget) / float(rest_rounds)
    # print(budget_for_round)
    percentage = prob * 100
    if 0 <= percentage < 40:
        answer1 = budget_for_round * 30 / 100
        answer2 = budget_for_round * 40 / 100
    elif 40 <= percentage <= 60:
        answer1 = budget_for_round * 40 / 100
        answer2 = budget_for_round * 70 / 100
    elif 60 <= percentage <= 100:
        answer1 = budget_for_round
        answer2 = budget_for_round
    else:
        failed_status("percentage is either negative or greater than 100")
    answer = (answer2 + answer1) / 2
    # we need to get answer from ui

    if len(histories) > 1:
        penultimate_history = History.objects.filter(~Q(id=history.id)).reverse().first()
        print(penultimate_history)

        if 60 > percentage > penultimate_history.click_prob * 100:
            will_be_increased = (percentage - penultimate_history.click_prob * 100) // 10
            answer += budget_for_round * will_be_increased / 100
            return answer
        elif not penultimate_history.win and penultimate_history.click_prob == prob:
            if answer + budget_for_round * 4 / 100 <= budget_for_round:
                answer += budget_for_round * 4 / 100
            return answer

    return answer

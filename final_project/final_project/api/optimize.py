from game.models import History
from .helper_functions import *


def betting_limit(budget, prob):
    histories = History.objects.all()
    percentage = prob * 100
    print(percentage)
    if 0 <= percentage < 40:
        answer1 = budget * 5 / 100
        answer2 = budget * 8 / 100
    elif 40 <= percentage <= 60:
        answer1 = budget * 8 / 100
        answer2 = budget * 10 / 100
    elif 60 <= percentage <= 100:
        answer1 = budget * 10 / 100
        answer2 = budget * 15 / 100
    else:
        return failed_status("percentage is either negative or greater than 100")
    answer = (answer2 + answer1) / 2
    # we need to get answer from ui

    if len(histories) > 1:
        history = History.objects.latest('id')
        penultimate_history = History.objects.filter(id=history.id).reverse().first()

        if 60 > percentage > history.click_prob * 100:
            will_be_increased = (percentage - history.click_prob * 100) // 10
            answer = history.price + budget * will_be_increased / 100
            return answer
        elif not history.win and not penultimate_history.win:
            answer += budget * 3 / 100
            return answer
        elif not history.win and history.click_prob == prob:
            answer += budget * 4 / 100
            return answer

    return answer

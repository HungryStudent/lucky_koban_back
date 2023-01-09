from yookassa import Configuration, Payment
from configs import SECRET_KEY, SHOP_ID, url
from core.schemas import Case

Configuration.configure(SHOP_ID, SECRET_KEY)


def gen_pay(user_id, case: Case):
    payment = Payment.create({
        "amount": {
            "value": case.price,
            "currency": "RUB"
        },
        "capture": True,

        "confirmation": {
            "type": "redirect",
            "return_url": f"{url}"
        },
        "description": f'Покупка кейса "{case.name}" на Lucky Koban',
        "metadata": {"user_id": user_id,
                     "case_id": case.id}
    })
    return payment.confirmation.confirmation_url

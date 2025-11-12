from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, User


def create_order(tickets: list[dict], username: str,
                 date: str = None) -> Order:

    selected_user = User.objects.get(username=username)

    with transaction.atomic():
        user_order = Order.objects.create(user=selected_user)

        if date is not None:
            user_order.created_at = date

        user_order.save()

        for ticket in tickets:
            Ticket.objects.create(order=user_order,
                                  movie_session_id=ticket["movie_session"],
                                  seat=ticket["seat"],
                                  row=ticket["row"])

    return user_order


def get_orders(username: str = None) -> QuerySet[Order]:

    if username is not None:
        user = get_user_model().objects.get(username=username)

        return Order.objects.filter(user=user)

    return Order.objects.all()

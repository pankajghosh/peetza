from microcosm_eventsource.event_types import EventType, event_info
from microcosm_eventsource.transitioning import any_of, nothing


class CustomerEventType(EventType):
    CustomerStartedOrder = event_info(
        follows=nothing(),
        requires=[
            "order_id"
        ]
    )

    CustomerStartedPizza = event_info(
        follows=any_of(
            "CustomerStartedOrder",
            "CustomerFinalizedPizza"
        ),
        requires=[
            "pizza_id",
        ]
    )

    CustomerChosePizzaType = event_info(
        follows=any_of(
            "CustomerStartedPizza"
        ),
        requires=[
            "pizza_type",
            "pizza_size",
        ]
    )

    CustomerAddedTopping = event_info(
        follows=any_of(
            "CustomerChosePizzaType"
        ),
        requires=[
            "topping_type",
        ]

    )

    CustomerFinalizedPizza = event_info(
        follows=any_of(
            "CustomerChosePizzaType",
            "CustomerAddedTopping",
        ),
    )

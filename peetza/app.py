"""
Create the application.

"""
from microcosm.api import create_object_graph
from microcosm.loaders import load_each, load_from_environ, load_from_json_file
from microcosm.loaders.compose import load_config_and_secrets
from microcosm_secretsmanager.loaders.conventions import load_from_secretsmanager

import peetza.postgres  # noqa
import peetza.routes.pizza.controller  # noqa
import peetza.routes.pizza.crud     # noqa
import peetza.stores.pizza_store    # noqa
import peetza.routes.topping.controller # noqa
import peetza.routes.topping.crud   # noqa
import peetza.stores.topping_store  # noqa
import peetza.routes.order.crud     # noqa
import peetza.routes.order.controller   # noqa
import peetza.stores.order_store    # noqa
from peetza.config import load_default_config


def create_app(debug=False, testing=False, model_only=False):
    """
    Create the object graph for the application.

    """
    config_loader = load_each(
        load_default_config,
        load_from_environ,
        load_from_json_file,
    )
    partitioned_loader = load_config_and_secrets(
        config=config_loader,
        secrets=load_from_secretsmanager(),
    )

    graph = create_object_graph(
        name=__name__.split(".")[0],
        debug=debug,
        testing=testing,
        loader=partitioned_loader,
    )

    graph.use(
        "pizza_store",
        "topping_store",
        "order_store",
        "logging",
        "postgres",
        "sessionmaker",
        "session_factory",
    )

    if not model_only:
        graph.use(
            # conventions
            "build_info_convention",
            "config_convention",
            "discovery_convention",
            "health_convention",
            "landing_convention",
            "port_forwarding",
            "postgres_health_check",
            "swagger_convention",
            # routes
            "pizza_routes",
            "topping_routes",
            "order_routes",
        )

    return graph.lock()

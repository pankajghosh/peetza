from microcosm_postgres.models import EntityMixin, Model


class Order(EntityMixin, Model):
    __tablename__ = "order"

from ..controllers import orders as controller
import pytest
from ..models import orders as model

@pytest.fixture
def db_session():
    class _FakeQuery:
        def __init__(self, result=None):
            self._result = result

        def filter(self, *args, **kwargs):
            return self

        def first(self):
            return self._result

    class _FakeSession:
        def __init__(self, promo=None):
            self._query = _FakeQuery(promo)
            self.added = []
            self.committed = False

        def query(self, *_args, **_kwargs):
            return self._query

        def add(self, obj):
            self.added.append(obj)

        def commit(self):
            self.committed = True

        def refresh(self, _obj):
            return None

    return _FakeSession()


def test_create_order(db_session):
    # Create a sample order
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order"
    }

    order_object = model.Order(**order_data)

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"

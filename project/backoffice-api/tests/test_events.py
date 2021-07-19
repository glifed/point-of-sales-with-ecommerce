from datetime import datetime

import pytest
from app.event.event import EventHandler
from app.resources.events import Events


@pytest.fixture(scope='module')
def fn():
    return lambda data: data

@pytest.fixture(scope='function')
def fake_data(fake_name):
    return {'user': fake_name, 'created_by': fake_name, 'timestamp': datetime.utcnow()}

event = EventHandler()

def test_can_subscribe(fn):
    event.subscribe(Events.CREATE_USER, fn)
    
    assert fn in event.subscribers[Events.CREATE_USER]

def test_can_unsusbcribe(fn):
    event.unsubscribe(Events.CREATE_USER, fn)

    assert fn not in event.subscribers[Events.CREATE_USER]
    

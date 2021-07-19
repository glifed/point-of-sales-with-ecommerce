from types import FunctionType
from typing import Any


class EventHandler:
    """Implementation of Observer Pattern.
    Handle events and notify subscribers to those events.
    """
    subscribers = dict()

    def subscribe(self, event_type: str, fn: FunctionType) -> None:
        if not event_type in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(fn)
    
    def emit(self, event_type: str, data: Any) -> None:
        if not event_type in self.subscribers:
            return
        for fn in self.subscribers[event_type]:
            fn(data)
    
    def unsubscribe(self, event_type: str, fn: FunctionType) -> None:
        if not event_type in self.subscribers:
            return
        fn_indx = self.subscribers[event_type].index(fn)
        self.subscribers[event_type].pop(fn_indx)

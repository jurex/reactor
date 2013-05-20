#
# eventmanager.py
#

from reactor import log, component

class EventManager(component.Component):
    def __init__(self):
        component.Component.__init__(self, "EventManager")
        self.handlers = {}

    def fireEvent(self, event):
        """
        Emits the event to interested clients.

        :param event: WhistlerEvent
        """
        # Call any handlers for the event
        if event.name in self.handlers:
            for handler in self.handlers[event.name]:
                log.debug("running handler %s for event %s with args: %s", event.name, handler, event.args)
                handler(*event.args)

    def registerEventHandler(self, event, handler):
        """
        Registers a function to be called when a `:param:event` is emitted.

        :param event: str, the event name
        :param handler: function, to be called when `:param:event` is emitted

        """
        if event not in self.handlers:
            self.handlers[event] = []

        if handler not in self.handlers[event]:
            #log.debug('event handler registred: ' + str(handler))
            self.handlers[event].append(handler)
            
    def unregisterEventHandler(self, event, handler):
        """
        Deregisters an event handler function.

        :param event: str, the event name
        :param handler: function, currently registered to handle `:param:event`

        """
        if event in self.handlers and handler in self.handlers[event]:
            self.handlers[event].remove(handler)
#
# component.py
#

from reactor import log

class ComponentAlreadyRegistered(Exception):
    pass

class Component(object):

    def __init__(self, name, depend=None):
        self._component_name = name
        self._component_depend = depend
        self._component_state = "Stopped"
        componentManager.register(self)


    def _component_start(self):
        if self._component_state == "Stopped":
            if hasattr(self, "start"):
                self._component_state = "Starting"
                self.start()
                self._component_state = "Started"
                return True;
            else:
                return False
                
        elif self._component_state == "Started":
            return True
            

        log.error("Cannot start a component not in a Stopped state!")
        return False;

    def _component_stop(self):

        if self._component_state != "Stopped" and self._component_state != "Stopping":
            if hasattr(self, "stop"):
                self._component_state = "Stopping"
                self.stop()
                self._component_state = "Stopped"
                return True
            else:
                return False

        elif self._component_state == "Stopped":
            return True

        log.error("Cannot start a component not in a Started state!")
        return False

    def _component_shutdown(self):

        if hasattr(self, "shutdown"):
            return self.shutdown()
        
        return self._component_stop()

class ComponentManager(object):

    def __init__(self):
        self.components = {}

    def register(self, obj):
        """
        Registers a component object with the registry.  This is done
        automatically when a Component object is instantiated.

        :param obj: the Component object
        :type obj: object

        :raises ComponentAlreadyRegistered: if a component with the same name is already registered.

        """
        name = obj._component_name
        if name in self.components:
            raise ComponentAlreadyRegistered("Component already registered with name %s" % name)

        self.components[obj._component_name] = obj

    def unregister(self, name):
        """
        unregisters a component from the registry.  A stop will be
        issued to the component prior to deregistering it.

        :param name: the name of the component
        :type name: string

        """

        if name in self.components:
            log.debug("Unregistering Component: %s", name)
            self.stop([name])
            del self.components[name]

    def start(self, names=[]):
        if not names:
            names = self.components.keys()
        elif isinstance(names, str):
            names = [names]

        for name in names:
            self.components[name]._component_start()

    def stop(self, names=[]):
        if not names:
            names = self.components.keys()
        elif isinstance(names, str):
            names = [names]

        for name in names:
            self.components[name]._component_stop()

    def shutdown(self):
        names = self.components.keys()

        for name in names:
            self.components[name]._component_shutdown()


componentManager = ComponentManager()

def get(name):
    """
    Return a reference to a component.

    :param name: the Component name to get
    :type name: string

    :returns: the Component object
    :rtype: object

    :raises KeyError: if the Component does not exist

    """
    return componentManager.components[name]
from ..core.state import StateBase, TerminateState
from ..native.memory import MemoryException


class State(StateBase):
    @property
    def cpu(self):
        """
        Current cpu state
        """
        return self._platform.current

    @property
    def mem(self):
        """
        Current virtual memory mappings
        """
        return self._platform.current.memory

    def execute(self):
        """
        Perform a single step on the current state
        """
        try:
            result = self._platform.execute()
        except MemoryException as e:
            raise TerminateState(str(e), testcase=True)

        # Remove when code gets stable?
        assert self.platform.constraints is self.constraints

        return result

    def invoke_model(self, model):
        """
        Invokes a `model`. Modelling can be used to override a function in the target program with a custom
        implementation.

        For more information on modelling see docs/models.rst

        A `model` is a callable whose first argument is a `manticore.native.State` instance.
        If the following arguments correspond to the arguments of the C function
        being modeled. If the `model` models a variadic function, the following argument
        is a generator object, which can be used to access function arguments dynamically.
        The `model` callable should simply return the value that should be returned by the
        native function being modeled.f

        :param model: callable, model to invoke
        """
        self._platform.invoke_model(model, prefix_args=(self,))

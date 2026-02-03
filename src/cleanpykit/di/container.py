from typing import Type, Any, Dict

class Container:
    def __init__(self):
        self._bindings: Dict[Type, Type] = {}
        self._instances: Dict[Type, Any] = {}

    def bind(self, cls: Type, impl: Type | None = None, singleton: bool = True):
        """
        Bind a class to an implementation
        - cls: the abstract class or key
        - impl: concrete class (if None, cls itself)
        - singleton: whether to reuse the same instance
        """
        self._bindings[cls] = (impl or cls, singleton)
    
    def resolve(self, cls: Type) -> Any:
        """
        Return an instance of the bound class
        - Raises KeyError if not bound
        """
        if cls not in self._bindings:
            raise KeyError(f"Dependency {cls.__name__} not bound in container")
        
        impl, singleton = self._bindings[cls]
        if singleton and cls in self._instances:
            return self._instances[cls]
        
        kwargs = {}
        init_params = getattr(impl, "__annotations__", {})
        for name, typ in init_params.items():
            if typ in self._bindings:
                kwargs[name] = self.resolve(typ)
            
        instance = impl(**kwargs)

        if singleton:
            self._instances[cls] = instance
        
        return instance

    def override(self, cls: Type, instance: Any):
        """
        Override a binding with a specific instance (useful for tests)
        """
        self._instances[cls] = instance

        to_remove = []
        for k, v in self._instances.items():
            impl, singleton = self._bindings.get(k, (None, None))
            if singleton and hasattr(impl, "__annotations__"):
                if cls in impl.__annotations__.values():
                    to_remove.append(k)
        for k in to_remove:
            del self._instances[k]
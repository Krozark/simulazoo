from snecs import Query

__all__ = []


class SystemBase:
    COMPONENTS = ()

    def process(self, world):
        for entity, components in Query(component_types=self.COMPONENTS, world=world):
            self.process_entity(entity, components)

    def process_entity(self, entity, components):
        raise NotImplementedError

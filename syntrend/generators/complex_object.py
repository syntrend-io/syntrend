from syntrend.generators import register, PropertyGenerator, get_generator
from syntrend.config.model import PropertyDefinition

from random import randint


class BaseComplexGenerator(PropertyGenerator):
    def get_children(self) -> list[str]:
        raise NotImplementedError(
            f"{str(type(self))}: 'get_children' is not implemented"
        )


@register
class UnionGeneratorBase(BaseComplexGenerator):
    """Generates a single value based on a random selection of many provided generator options

    Args:
        items (list[`:obj:PropertyGenerator`]): List of generator types with their own properties

    Example:
        Selectively choose a generator randomly or through the use of an expression::

            type: union
            items:
                - type: integer
                  min_offset: -4
                  max_offset: 4
                - type: integer
                  min_offset: 10
                  max_offset: 20
    """

    name = 'union'

    def get_children(self):
        return []

    def load_items(self, items: list[any]) -> list[any]:
        _gens = []
        for item in items:
            _gens.append(
                get_generator(
                    self.root_object, PropertyDefinition(**item), self.root_manager
                )
            )
        return _gens

    def generate(self) -> any:
        return self.items[randint(0, len(self.items) - 1)].render()


@register
class ListGeneratorBase(BaseComplexGenerator):
    """Generates a list-object of 1 or many values of the specified generator type"""

    name = 'list'
    default_config = {
        'min_length': 1,
        'max_length': 5,
    }

    def get_children(self):
        return []

    def load_kwargs(self, kwargs):
        kwargs['min_length'] = int(kwargs['min_length'])
        kwargs['max_length'] = int(kwargs['max_length'])
        assert kwargs['min_length'] <= kwargs['max_length'], (
            'Min must be less than or equal to Max'
        )
        assert kwargs['min_length'] >= 0, 'List cannot have a negative length'
        assert 'sub_type' in kwargs, (
            "Must provide a 'sub_type' property for the values to be generated"
        )
        kwargs['sub_type'] = get_generator(
            self.root_object,
            PropertyDefinition(**kwargs['sub_type']),
            self.root_manager,
        )
        return kwargs

    def generate(self) -> list[any]:
        return [
            self.kwargs.sub_type.generate()
            for _ in range(randint(self.kwargs.min_length, self.kwargs.max_length))
        ]


@register
class ObjectGeneratorBase(BaseComplexGenerator):
    """Generates an object based on a defined mapping of properties"""

    name = 'object'
    type = dict

    def get_children(self) -> list[str]:
        return list(self.properties)

    def load_properties(
        self, properties: dict[str, any]
    ) -> dict[str, PropertyGenerator]:
        return {
            key: get_generator(self.root_object, properties[key], self.root_manager)
            for key in properties
        }

    def generate(self):
        for key in self.properties:
            self.properties[key].render()
        return {key: self.properties[key].render() for key in self.properties}

    def undo(self):
        super(BaseComplexGenerator, self).undo()
        for key in self.properties:
            self.properties[key].undo()

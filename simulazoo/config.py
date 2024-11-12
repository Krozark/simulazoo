import json
import logging

from jsonschema import validate

from . import components

logger = logging.getLogger(__name__)

schema = {
    "$schema": "http://json-schema.org/draft-06/schema#",
    "type": "object",
    "additionalProperties": False,
    "patternProperties": {
        "[A-Za-z0-9]+": {  # specie name
            "additionalProperties": False,
            "type": "object",
            "properties": {
                "components": {
                    "type": "array",
                    "items": {"type": "string", "enum": components.__all__},
                    "minItems": 1,
                },
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": True,
                    },
                },
            },
            "required": ["components", "entities"],
        }
    },
}


def parse_config_file(file):
    data = json.load(file)
    validate(instance=data, schema=schema)

    entities = []

    for specie_key, specie_data in data.items():
        component_classes = {components.LivingBeingComponent}
        # build components map
        for component_name in specie_data["components"]:
            component_class = getattr(components, component_name)
            component_classes.add(component_class)

        # for each entity build its components
        for entity_data in specie_data["entities"]:
            component_kwargs = {
                component_class: {} for component_class in component_classes
            }
            component_kwargs[components.LivingBeingComponent].update(
                {"specie": specie_key}
            )
            # for each attribute, search the matching component
            for attribute_key, attribute_value in entity_data.items():
                for component in component_classes:
                    if attribute_key in component.__slots__:
                        component_kwargs[component].update(
                            {attribute_key: attribute_value}
                        )
                        break
                else:
                    logger.error(
                        f"Unknown attribute {attribute_key} in component list {component_classes}. Skipping it."
                    )

            entities.append(component_kwargs)

    return entities

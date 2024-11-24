import io
import json

import pytest
from jsonschema import ValidationError

from simulazoo import components, config


def create_test_file(content):
    """Helper function to create a file-like object from a dictionary"""
    return io.BytesIO(json.dumps(content).encode('utf-8'))

def test_one_component():
    """Test with a simple valid configuration"""
    test_config = {
        "Fern": {
            "components": ["PlantComponent"],
            "entities": [{}]
        }
    }

    result = config.parse_config_file(create_test_file(test_config))

    assert len(result) == 1
    entity = result[0]

    assert components.LivingBeingComponent in result[0]
    assert components.PlantComponent in result[0]

    assert entity[components.LivingBeingComponent] == {"specie": "Fern"}
    assert entity[components.PlantComponent] == {}

def test_multiple_components():
    """Test with multiple components for a single species"""
    test_config = {
        "Lion": {
            "components": ["ZoophageComponent", "AnimalComponent"],
            "entities": [{
                "sex": "FEMALE",
                "name": "Alice",
                "age": 14
            }]
        }
    }

    result = config.parse_config_file(create_test_file(test_config))

    assert len(result) == 1
    entity = result[0]

    assert components.LivingBeingComponent in entity
    assert components.ZoophageComponent in entity
    assert components.AnimalComponent in entity

    assert entity[components.LivingBeingComponent] == {"specie": "Lion", "age": 14}
    assert entity[components.ZoophageComponent]=={}
    assert entity[components.AnimalComponent] == {
        "sex": "FEMALE",
        "name": "Alice"
    }


def test_multiple_entities():
    """Test with multiple entities for a single species"""
    test_config = {
        "Antelope": {
            "components": ["PhytophageComponent", "AnimalComponent"],
            "entities": [
                {"sex": "FEMALE"},
                {"sex": "MALE"}
            ]
        }
    }

    result = config.parse_config_file(create_test_file(test_config))

    assert len(result) == 2

    assert all(components.LivingBeingComponent in entity for entity in result)
    assert all(components.PhytophageComponent in entity for entity in result)
    assert all(components.AnimalComponent in entity for entity in result)

    assert all(entity[components.LivingBeingComponent] == {"specie": "Antelope"} for entity in result)
    assert all(entity[components.PhytophageComponent] == {} for entity in result)
    assert result[0][components.AnimalComponent]["sex"] == "FEMALE"
    assert result[1][components.AnimalComponent]["sex"] == "MALE"

def test_invalid_schema():
    """Test with invalid schema (missing required field)"""
    test_config = {
        "Invalid": {
            "entities": []  # Missing 'components' field
        }
    }

    with pytest.raises(ValidationError):
        config.parse_config_file(create_test_file(test_config))
#
def test_invalid_component():
    """Test with invalid component name"""
    test_config = {
        "Invalid": {
            "components": ["NonExistentComponent"],
            "entities": [{}]
        }
    }

    with pytest.raises(ValidationError):
        config.parse_config_file(create_test_file(test_config))

def test_unknown_attribute():
    """Test with unknown attribute in entity"""
    test_config = {
        "Lion": {
            "components": ["AnimalComponent"],
            "entities": [{
                "unknown_attribute": "value"  # This attribute doesn't exist in any component
            }]
        }
    }

    result = config.parse_config_file(create_test_file(test_config))
    assert len(result) == 1
    # Verify that the unknown attribute was not added to any component
    assert all(
        "unknown_attribute" not in component_data
            for component_data in result[0].values()
    )

def test_empty_entities():
    """Test with empty entities list"""
    test_config = {
        "Fern": {
            "components": ["PlantComponent"],
            "entities": []
        }
    }

    result = config.parse_config_file(create_test_file(test_config))
    assert len(result) == 0


def test_multiple_entities_same_species():
    """Test parsing of multiple entities of the same species"""
    test_config = {
        "Antelope": {
            "components": ["PhytophageComponent", "AnimalComponent"],
            "entities": [
                {"sex": "FEMALE", "name": "Ante1"},
                {"sex": "MALE", "name": "Ante2"},
                {"sex": "FEMALE", "name": "Ante3"}
            ]
        }
    }

    result = config.parse_config_file(create_test_file(test_config))

    assert len(result)==3

    assert all(components.LivingBeingComponent in entity for entity in result)
    assert all(components.PhytophageComponent in entity  for entity in result)
    assert all(components.AnimalComponent in entity  for entity in result)


    assert all(entity[components.LivingBeingComponent] == {"specie": "Antelope"} for entity in result)
    assert all(entity[components.PhytophageComponent]=={} for entity in result)

    assert result[0][components.AnimalComponent] == {"sex": "FEMALE", "name": "Ante1"}
    assert result[1][components.AnimalComponent] == {"sex": "MALE", "name": "Ante2"}
    assert result[2][components.AnimalComponent] == {"sex": "FEMALE", "name": "Ante3"}


def test_multiple_species():
    """Test with multiple species in the configuration"""
    test_config = {
        "Antelope": {
            "components": ["PhytophageComponent", "AnimalComponent"],
            "entities": [
                {"sex": "FEMALE"},
                {"sex": "MALE"}
            ]
        },
        "Lion": {
            "components": ["ZoophageComponent", "AnimalComponent"],
            "entities": [
                {"sex": "FEMALE", "name": "Alice"},
                {"sex": "MALE", "name": "Bob"}
            ]
        },
        "Fern": {
            "components": ["PlantComponent"],
            "entities": [
                {},
                {}
            ]
        }
    }

    result = config.parse_config_file(create_test_file(test_config))

    # Check total number of entities
    assert len(result) == 6  # 2 Antelope, 2 Lion, 2 Fern

    # Verify Antelope entities
    antelope_entities = result[:2]
    assert all(entity[components.LivingBeingComponent] == {"specie": "Antelope"} for entity in antelope_entities)
    assert all(components.PhytophageComponent in entity for entity in antelope_entities)
    assert all(components.AnimalComponent in entity for entity in antelope_entities)

    assert antelope_entities[0][components.AnimalComponent] == {"sex": "FEMALE"}
    assert antelope_entities[1][components.AnimalComponent] == {"sex":  "MALE"}

    # Verify Lion entities
    lion_entities = result[2:4]
    assert all(entity[components.LivingBeingComponent] == {"specie": "Lion"} for entity in lion_entities)
    assert all(components.ZoophageComponent in entity for entity in lion_entities)
    assert all(components.AnimalComponent in entity for entity in lion_entities)

    assert lion_entities[0][components.AnimalComponent] == {"sex": "FEMALE", "name": "Alice"}
    assert lion_entities[1][components.AnimalComponent] == {"sex": "MALE", "name": "Bob"}

    # Verify Fern entities
    fern_entities = result[4:]
    assert all(entity[components.LivingBeingComponent] == {"specie": "Fern"} for entity in fern_entities)
    assert all(components.PlantComponent in entity for entity in fern_entities)
    assert all(entity[components.PlantComponent] == {} for entity in fern_entities)

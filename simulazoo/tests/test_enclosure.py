import json
from io import StringIO
from unittest import mock

from snecs import Query, all_components

from simulazoo.components import (AnimalComponent, LivingBeingComponent, PlantComponent)
from simulazoo.enclosure import Enclosure, fill_default_enclosure
from simulazoo.enums import SexEnum


def test_create_entity():
    """Test entity creation with components in the enclosure."""
    enclosure = Enclosure("Test Enclosure")
    entity = enclosure.create_entity(
        LivingBeingComponent(specie="Lion"),
        AnimalComponent(name="Simba", sex=SexEnum.MALE)
    )

    assert entity is not None

    components = all_components(entity, world=enclosure.world)

    assert len(components) == 2
    assert isinstance(components[LivingBeingComponent], LivingBeingComponent)
    assert isinstance(components[AnimalComponent], AnimalComponent)

    assert components[LivingBeingComponent].specie == "Lion"
    assert components[AnimalComponent].name == "Simba"
    assert components[AnimalComponent].sex == SexEnum.MALE

def test_empty_report():
    """Test report generation for an empty enclosure."""
    enclosure = Enclosure("Empty Enclosure")
    report = enclosure.build_report()

    expected_report = (
        "==== Report of enclosure Empty Enclosure: day 0 ===\n"
        "Plant (0):\n"
        "Animals (0):\n"
        "===================="
    )
    assert report.strip() == expected_report.strip()

def test_process_day_with_report():
    """Test processing a day and generating a report."""
    enclosure = Enclosure("Process day Enclosure")
    with mock.patch.object(enclosure, "log_report") as log_report_mock:
        enclosure.process_day(log_report=True)
        log_report_mock.assert_called_once()

    assert enclosure.day == 1


def test_fill_default_enclosure():
    """Test the default entities are added correctly."""
    enclosure = Enclosure("Default Enclosure")
    fill_default_enclosure(enclosure)

    # Verify the number of plants
    plant_entities = [
        entity for entity, components in Query(component_types=(LivingBeingComponent, PlantComponent), world=enclosure.world)
    ]
    assert len(plant_entities) == 4  # 3 Ferns + 1 Oak tree

    # Verify the number of animals
    animal_entities = [
        entity for entity, components in Query(component_types=(LivingBeingComponent, AnimalComponent), world=enclosure.world)
    ]
    assert len(animal_entities) == 13  # Total animals added in fill_default_enclosure

def test_load_from_config_file():
    """Test loading entities from a configuration file."""
    config_data = {
        "Lion": {
            "components": ["ZoophageComponent", "AnimalComponent"],
            "entities": [
                {"name": "Simba", "sex": "MALE"},
                {"name": "Nala", "sex": "FEMALE"}
            ]
        },
        "Fern": {
            "components": ["PlantComponent"],
            "entities": [{}]
        }
    }
    buffer = StringIO(json.dumps(config_data))

    enclosure = Enclosure("Config Enclosure")
    enclosure.load_from_config_file(buffer)

    lion_entities = [
        entity for entity, components in Query(component_types=(LivingBeingComponent,), world=enclosure.world)
        if components[0].specie == "Lion"
    ]
    assert len(lion_entities) == 2

    fern_entities = [
        entity for entity, components in Query(component_types=(LivingBeingComponent,), world=enclosure.world)
        if components[0].specie == "Fern"
    ]
    assert len(fern_entities) == 1

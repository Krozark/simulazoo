from unittest.mock import MagicMock

from snecs import (
    World,
    new_entity
)

from simulazoo.components import (
    AnimalComponent,
    LivingBeingComponent,
    PlantComponent,
)
from simulazoo.report import EnclosureReportBuilder


def test_empty_enclosure():
    """Test report generation for an empty enclosure."""
    world = World()
    enclosure = MagicMock(name="EnclosureMock")
    enclosure.name = "Empty Enclosure"
    enclosure.day = 1
    enclosure.world = world

    report_builder = EnclosureReportBuilder(enclosure)

    report = report_builder.build_repport().getvalue()

    expected_report = (
        "==== Report of enclosure Empty Enclosure: day 1 ===\n"
        "Plant (0):\n"
        "Animals (0):\n"
        "===================="
    )
    assert report.strip() == expected_report.strip()


def test_enclosure_with_plants():
    """Test report generation for an enclosure with plants only."""
    world = World("Plant Enclosure")

    # Add plants to the world
    new_entity(components=(LivingBeingComponent(specie="Fern", hp=10, age=2), PlantComponent()), world=world)
    new_entity(components=(LivingBeingComponent(specie="Oak Tree", hp=12, age=5), PlantComponent()), world=world)

    enclosure = MagicMock(name="EnclosureMock")
    enclosure.name = "Plant Enclosure"
    enclosure.day = 1
    enclosure.world = world

    report_builder = EnclosureReportBuilder(enclosure)

    report = report_builder.build_repport().getvalue()

    expected_report = (
        "==== Report of enclosure Plant Enclosure: day 1 ===\n"
        "Plant (2):\n"
        " - Specie: Fern, HP 10, Age 2\n"
        " - Specie: Oak Tree, HP 12, Age 5\n"
        "Animals (0):\n"
        "===================="
    )
    assert report.strip() == expected_report.strip()
#

def test_enclosure_with_animals():
    """Test report generation for an enclosure with animals only."""
    world = World()

    # Add animals to the world
    new_entity(components=(LivingBeingComponent(specie="Lion", hp=80, age=5), AnimalComponent(name="Leo", sex="MALE")) , world=world)
    new_entity(components=(LivingBeingComponent(specie="Elephant", hp=200, age=10), AnimalComponent(name="Ella", sex="FEMALE")), world=world)

    enclosure = MagicMock(name="EnclosureMock")
    enclosure.name = "Animal Enclosure"
    enclosure.day = 2
    enclosure.world = world

    report_builder = EnclosureReportBuilder(enclosure)

    report = report_builder.build_repport().getvalue()

    expected_report = (
        "==== Report of enclosure Animal Enclosure: day 2 ===\n"
        "Plant (0):\n"
        "Animals (2):\n"
        " - Name: Leo, Sex: MALE, Specie: Lion, HP 80, Age 5\n"
        " - Name: Ella, Sex: FEMALE, Specie: Elephant, HP 200, Age 10\n"
        "===================="
    )
    assert report.strip() == expected_report.strip()


def test_enclosure_with_plants_and_animals():
    """Test report generation for an enclosure with both plants and animals."""
    world = World()

    # Add plants to the world
    new_entity(components=(LivingBeingComponent(specie="Fern", hp=100, age=3),PlantComponent()), world=world)

    # Add animals to the world
    new_entity(components=(LivingBeingComponent(specie="Tiger", hp=150, age=6),AnimalComponent(name="Tigra", sex="FEMALE")), world=world)

    enclosure = MagicMock(name="EnclosureMock")
    enclosure.name = "Mixed Enclosure"
    enclosure.day = 3
    enclosure.world = world

    report_builder = EnclosureReportBuilder(enclosure)

    report = report_builder.build_repport().getvalue()

    expected_report = (
        "==== Report of enclosure Mixed Enclosure: day 3 ===\n"
        "Plant (1):\n"
        " - Specie: Fern, HP 100, Age 3\n"
        "Animals (1):\n"
        " - Name: Tigra, Sex: FEMALE, Specie: Tiger, HP 150, Age 6\n"
        "===================="
    )
    assert report.strip() == expected_report.strip()

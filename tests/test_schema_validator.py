from src.etl.schema_validator import SchemaValidator


def test_validator_creation():
    validator = SchemaValidator()

    assert len(validator.failures) == 0


def test_add_failure():
    validator = SchemaValidator()

    validator.add_failure(
        "DQ-01",
        "CRITICAL",
        "companies",
        "id",
        "Null Primary Key",
        5,
    )

    assert len(validator.failures) == 1


def test_failure_rule_id():
    validator = SchemaValidator()

    validator.add_failure(
        "DQ-02",
        "CRITICAL",
        "companies",
        "id",
        "Duplicate PK",
        2,
    )

    assert validator.failures[0]["rule_id"] == "DQ-02"

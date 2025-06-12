from pharmdb_extended import PharmaDB

db = PharmaDB()

# Pusta baza
assert db.list_drugs_with_side_effect_frequency(0, 100) == []
assert db.count_drugs_with_side_effect_frequency(0, 100) == 0

print("Test pustej bazy przeszedł poprawnie")

# Dodawanie elementów od najmniejszej częstotliwości
db.add_drug(
    "Drug_A",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_A", 1, 5.0),
        ("effect_B", 2, 10.0),
    ]
)

db.add_drug(
    "Drug_B",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_A", 1, 15.0),
    ]
)
db.add_drug(
    "Drug_C",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_C", 3, 20.0),
        ("effect_B", 2, 30.0),
    ]
)

db.add_drug(
    "Drug_D",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_A", 1, 31.0),
        ("effect_C", 1, 32.0),
        ("effect_D", 2, 33.0)
    ]
)


assert db.count_drugs_with_side_effect_frequency(0, 100) == 8
assert db.count_drugs_with_side_effect_frequency(
    5.0, 15.0) == 3
assert db.count_drugs_with_side_effect_frequency(
    0, 3) == 0
assert db.count_drugs_with_side_effect_frequency(
    9.9, 10.1) == 1

assert db.count_drugs_with_side_effect_frequency(
    23, 25) == 0


assert db.count_drugs_with_side_effect_frequency(35, 40) == 0

print("Zwrócono:", sorted(db.list_drugs_with_side_effect_frequency(0, 100)))
assert sorted(db.list_drugs_with_side_effect_frequency(0, 100)) == [
    ("Drug_A", "effect_A"),
    ("Drug_A", "effect_B"),
    ("Drug_B", "effect_A"),
    ("Drug_C", "effect_B"),
    ("Drug_C", "effect_C"),
    ("Drug_D", "effect_A"),
    ("Drug_D", "effect_C"),
    ("Drug_D", "effect_D")]
assert sorted(db.list_drugs_with_side_effect_frequency(5.0, 15.0)) == [
    ("Drug_A", "effect_A"),
    ("Drug_A", "effect_B"),
    ("Drug_B", "effect_A")]

assert sorted(db.list_drugs_with_side_effect_frequency(0, 3)) == []

assert sorted(db.list_drugs_with_side_effect_frequency(9.9, 10.1)) == [
    ("Drug_A", "effect_B")]
assert db.list_drugs_with_side_effect_frequency(34, 35) == []

print("Pierwsza faza testów przeszła poprawnie")


# Dodawanie elementów według malejącej częstotliwośći

db = PharmaDB()

db.add_drug(
    "Drug_D",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_D", 1, 33.0),
        ("effect_C", 1, 32.0),
        ("effect_A", 2, 31.0)
    ]
)


db.add_drug(
    "Drug_C",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_B", 2, 30.0),
        ("effect_C", 3, 20.0)
    ]
)

db.add_drug(
    "Drug_B",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_A", 1, 15.0),
    ]
)


db.add_drug(
    "Drug_A",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_B", 2, 10.0),
        ("effect_A", 1, 5.0)
    ]
)


assert db.count_drugs_with_side_effect_frequency(0, 100) == 8
assert db.count_drugs_with_side_effect_frequency(
    5.0, 15.0) == 3
assert db.count_drugs_with_side_effect_frequency(
    0, 3) == 0
assert db.count_drugs_with_side_effect_frequency(
    9.9, 10.1) == 1

assert db.count_drugs_with_side_effect_frequency(
    23, 25) == 0


assert db.count_drugs_with_side_effect_frequency(34, 35) == 0


assert sorted(db.list_drugs_with_side_effect_frequency(0, 100)) == [
    ("Drug_A", "effect_A"),
    ("Drug_A", "effect_B"),
    ("Drug_B", "effect_A"),
    ("Drug_C", "effect_B"),
    ("Drug_C", "effect_C"),
    ("Drug_D", "effect_A"),
    ("Drug_D", "effect_C"),
    ("Drug_D", "effect_D")]
assert sorted(db.list_drugs_with_side_effect_frequency(5.0, 15.0)) == [
    ("Drug_A", "effect_A"),
    ("Drug_A", "effect_B"),
    ("Drug_B", "effect_A")]

assert sorted(db.list_drugs_with_side_effect_frequency(0, 3)) == []

assert sorted(db.list_drugs_with_side_effect_frequency(9.9, 10.1)) == [
    ("Drug_A", "effect_B")]
assert db.list_drugs_with_side_effect_frequency(34, 35) == []
print("Druga faza testów przeszła poprawnie")


# wstawianie elementów w środku przedziałów.

db = PharmaDB()

db.add_drug(
    "Drug_A",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_D", 1, 33.0),
    ]
)

db.add_drug(
    "Drug_B",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_A", 1, 5.0)
    ]
)

db.add_drug(
    "Drug_C",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_B", 2, 30.0),
        ("effect_C", 3, 20.0)
    ]
)

db.add_drug(
    "Drug_D",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_A", 1, 15.0),
    ]
)

db.add_drug(
    "Drug_E",
    indications=[],
    substitutes=[],
    side_effects=[
        ("effect_A", 1, 10.0),
        ("effect_C", 2, 32.0),
        ("effect_B", 1, 31.0)

    ]
)
assert db.count_drugs_with_side_effect_frequency(0, 100) == 8
assert db.count_drugs_with_side_effect_frequency(
    5.0, 15.0) == 3
assert db.count_drugs_with_side_effect_frequency(
    0, 3) == 0
assert db.count_drugs_with_side_effect_frequency(
    9.9, 10.1) == 1
assert db.count_drugs_with_side_effect_frequency(
    23, 25) == 0

assert db.count_drugs_with_side_effect_frequency(34, 35) == 0


assert sorted(db.list_drugs_with_side_effect_frequency(0, 100)) == [
    ("Drug_A", "effect_D"),
    ("Drug_B", "effect_A"),
    ("Drug_C", "effect_B"),
    ("Drug_C", "effect_C"),
    ("Drug_D", "effect_A"),
    ("Drug_E", "effect_A"),
    ("Drug_E", "effect_B"),
    ("Drug_E", "effect_C")]
assert sorted(db.list_drugs_with_side_effect_frequency(5.0, 15.0)) == [
    ("Drug_B", "effect_A"),
    ("Drug_D", "effect_A"),
    ("Drug_E", "effect_A")]

assert sorted(db.list_drugs_with_side_effect_frequency(0, 3)) == []

assert sorted(db.list_drugs_with_side_effect_frequency(9.9, 10.1)) == [
    ("Drug_E", "effect_A")]
assert db.list_drugs_with_side_effect_frequency(34, 35) == []


print("Wszystkie testy przeszły poprawnie")

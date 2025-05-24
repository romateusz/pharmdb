# Przykładowe testy dla projektu PharmDB z ASD 2025
from pharmdb import PharmDB

print('Testowanie minimalnej funkcjonalności...')
db = PharmDB()
drug1 = db.add_drug("Apap", [("ból głowy", 8), ("gorączka", 7)], [], 
                    [("senność", 1, 5.0), ("nudności", 2, 2.0)])

drug2 = db.add_drug("Ibuprom", [("ból głowy", 7), ("gorączka", 8), ("stany zapalne", 9)], [], 
                     [("ból brzucha", 2, 10.0), ("zawroty głowy", 1, 3.0)])

drug3 = db.add_drug("Aspiryna", [("ból głowy", 6), ("gorączka", 6)], [drug1, drug2], 
                     [("krwawienie", 3, 1.0), ("ból brzucha", 2, 15.0)])

# Testowanie number_of_indications
assert db.number_of_indications(drug1, 7) == 2
assert db.number_of_indications(drug1, 8) == 1
assert db.number_of_indications(drug2, 8) == 2
assert db.number_of_indications(drug3, 7) == 0

# Testowanie number_of_alternative_drugs
assert db.number_of_alternative_drugs(drug1) == 1  # Tylko Aspiryna może zastąpić Apap
assert db.number_of_alternative_drugs(drug2) == 1  # Tylko Aspiryna może zastąpić Ibuprom
assert db.number_of_alternative_drugs(drug3) == 0  # Nic nie może zastąpić Aspiryny

# Testowanie risk_score
assert db.risk_score(drug1) == 1*5.0 + 2*2.0  # senność (1*5.0) + nudności (2*2.0) = 9.0
assert db.risk_score(drug2) == 2*10.0 + 1*3.0  # ból brzucha (2*10.0) + zawroty głowy (1*3.0) = 23.0
assert db.risk_score(drug3) == 3*1.0 + 2*15.0  # krwawienie (3*1.0) + ból brzucha (2*15.0) = 33.0

# Testowanie find_best_alternative
assert db.find_best_alternative(drug1, 1) == drug1  # Tylko Apap i Aspiryna, Apap ma niższe ryzyko
assert db.find_best_alternative(drug2, 1) == drug2  # Tylko Ibuprom i Aspiryna, Ibuprom ma niższe ryzyko
print('Testy minimalnej funkcjonalności zakończone sukcesem!')

print('Testowanie pozostałej funkcjonalności (1/2)...')
# Dodajemy więcej leków do testowania
drug4 = db.add_drug("Paracetamol", [("ból głowy", 9), ("gorączka", 9)], [drug3], 
                     [("wysypka", 2, 1.0)])

drug5 = db.add_drug("Nurofen", [("ból głowy", 8), ("stany zapalne", 9)], [drug2, drug4], 
                    [("senność", 1, 3.0)])

drug6 = db.add_drug("Polopiryna", [("ból głowy", 5), ("gorączka", 5)], [drug3], 
                    [("krwawienie", 3, 0.5), ("wymioty", 2, 5.0)])

# Testowanie worst_side_effect
assert db.worst_side_effect(drug1) == "nudności"  # Najwyższy poziom to 2: "nudności"
assert db.worst_side_effect(drug2) == "ból brzucha"  # Najwyższy poziom to 2: "ból brzucha"
assert db.worst_side_effect(drug3) == "krwawienie"  # Najwyższy poziom to 3: "krwawienie"
assert db.worst_side_effect(drug6) == "krwawienie"  # Najwyższy poziom to 3: "krwawienie"

# Testowanie find_best_drug_for_indication
assert db.find_best_drug_for_indication("ból głowy") == drug4  # Paracetamol ma najwyższą skuteczność (9)
assert db.find_best_drug_for_indication("gorączka") == drug4  # Paracetamol ma najwyższą skuteczność (9)
assert db.find_best_drug_for_indication("stany zapalne") == drug5  # Nurofen ma tę samą skuteczność co Ibuprom (9), ale został dodany później

# Testowanie longest_alternative_list
assert db.longest_alternative_list() == [drug1, drug3, drug4, drug5]

print('Testy funkcjonalności (1/2) zakończone sukcesem!')

print('Testowanie pozostałej funkcjonalności (2/2)...')
# Tworzymy nową bazę danych do testowania update_best_indication
db2 = PharmDB()
d1 = db2.add_drug("Lek1", [("choroba A", 5), ("choroba B", 6)], [], [])
d2 = db2.add_drug("Lek2", [("choroba A", 7), ("choroba B", 5)], [], [])
d3 = db2.add_drug("Lek3", [("choroba A", 7), ("choroba B", 8)], [], [])

# Sprawdzamy najlepszy lek dla choroby A
assert db2.find_best_drug_for_indication("choroba A") == d3  # Lek3, bo ma skuteczność 7 i został dodany po Lek2

# Aktualizujemy najlepszy lek
db2.update_best_indication("choroba A", 8)

# Sprawdzamy czy aktualizacja została uwzględniona
assert db2.find_best_drug_for_indication("choroba A") == d3  # Nadal Lek3, ale teraz ze skutecznością 8

# Dodajemy nowy lek z taką samą skutecznością
d4 = db2.add_drug("Lek4", [("choroba A", 8)], [], [])

# Sprawdzamy czy nowy lek jest teraz najlepszy (ponieważ został dodany później)
assert db2.find_best_drug_for_indication("choroba A") == d4

# Testowanie find_best_alternative z większą liczbą kroków
# Tworzymy nową bazę danych
db3 = PharmDB()
a1 = db3.add_drug("A1", [], [], [("efekt", 1, 10.0)])  # risk_score = 10
a2 = db3.add_drug("A2", [], [a1], [("efekt", 1, 5.0)])  # risk_score = 5
a3 = db3.add_drug("A3", [], [a2], [("efekt", 1, 15.0)])  # risk_score = 15
a4 = db3.add_drug("A4", [], [a3], [("efekt", 1, 3.0)])  # risk_score = 3
a5 = db3.add_drug("A5", [], [a4], [("efekt", 1, 8.0)])  # risk_score = 8

# Z max_steps=1, a1 może być zastąpiony tylko przez a2
assert db3.find_best_alternative(a1, 1) == a2

# Z max_steps=2, a1 może być zastąpiony przez a2 i a3, a a2 ma niższe ryzyko
assert db3.find_best_alternative(a1, 2) == a2

# Z max_steps=3, a1 może być zastąpiony przez a2, a3 i a4, a a4 ma najniższe ryzyko
assert db3.find_best_alternative(a1, 3) == a4

# Z max_steps=4, a1 może być zastąpiony przez a2, a3, a4 i a5, a a4 ma najniższe ryzyko
assert db3.find_best_alternative(a1, 4) == a4

# Testowanie longest_alternative_list
assert db3.longest_alternative_list() == [a1, a2, a3, a4, a5]

print('Wszystkie testy zakończone sukcesem!')

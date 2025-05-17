from pharmdb import PharmDB

def run_all_tests():
    db = PharmDB()

    # Dodajemy 9 leków z różnymi właściwościami
    lek1 = db.add_drug("Apap", [("ból głowy", 8), ("gorączka", 7)], None, [("nudności", 1, 2.0)])
    lek2 = db.add_drug("Ibuprom", [("ból głowy", 9)], [lek1], [("zawroty głowy", 2, 3.0)])
    lek3 = db.add_drug("Pyralgina", [("gorączka", 6)], [lek1], [("nudności", 2, 7.0), ("wymioty", 3, 2.0)])
    lek4 = db.add_drug("Metafen", [("ból głowy", 6), ("gorączka", 8)], [lek3], [("senność", 1, 12.0)])
    lek5 = db.add_drug("Ketonal", [("ból zęba", 10)], None, [("senność", 1, 6.0)])
    lek6 = db.add_drug("Nurofen", [("ból głowy", 9)], [lek1, lek2], [("ból brzucha", 3, 1.0)])
    lek7 = db.add_drug("Polopiryna", [("gorączka", 7), ("ból gardła", 5)], [lek1], [("wymioty", 2, 5.0)])
    lek8= db.add_drug("Solpadeine", [("ból głowy", 8)], [lek6], [("senność", 1, 10.0)])
    lek9 = db.add_drug("Magnefar", [("skurcze", 9)], [], [])

    # number_of_indications
    assert db.number_of_indications(lek1, 7) == 2
    assert db.number_of_indications(lek3, 7) == 0

    # number_of_alternative_drugs
    assert db.number_of_alternative_drugs(lek1) == 4
    assert db.number_of_alternative_drugs(lek3) == 1

    # worst_side_effect
    assert db.worst_side_effect(lek3) == "wymioty"
    assert db.worst_side_effect(lek9) is None

    # risk_score
    assert round(db.risk_score(lek3), 2) == 20.0
    assert db.risk_score(lek9) == 0.0

    # find_best_alternative
    assert db.find_best_alternative(lek2) == lek1
    assert db.find_best_alternative(lek8) == lek1
    assert db.find_best_alternative(lek8, max_steps=1) == lek6

    # longest_alternative_list
    expected = [lek8, lek6, lek2, lek1]
    assert db.longest_alternative_list() == expected

    # find_best_drug_for_indication
    assert db.find_best_drug_for_indication("ból głowy") == lek6
    assert db.find_best_drug_for_indication("skurcze") == lek9

    # update_best_indication
    db.update_best_indication("ból głowy", 10)
    assert db.find_best_drug_for_indication("ból głowy") == lek6

    print("Wszystkie testy przeszły poprawnie.")

if __name__ == "__main__":
    run_all_tests()
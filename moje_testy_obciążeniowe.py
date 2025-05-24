from pharmdb import PharmDB
import time
import random
import string

def random_name(length=6):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

print("Przygotowanie testu obciążeniowego...")

db = PharmDB()

N = 100000  # liczba leków
max_neighbors = 300  # maksymalna liczba zamienników na lek

# Dodajemy leki z losowymi wskazaniami i efektami ubocznymi
drugs = []
for i in range(N):
    name = f"Drug_{i}"
    indications = [("choroba" + str(random.randint(1, 20)), random.randint(1, 10))]
    side_effects = [(random_name(), random.randint(1, 3), random.uniform(0.5, 10.0))]
    # Zamienniki dodamy potem
    drug_id = db.add_drug(name, indications, [], side_effects)
    drugs.append(drug_id)

# Teraz tworzymy reverse_substitutes (zamienniki)
# Każdy lek może mieć do max_neighbors leków, które go zastępują (losowo)
for i in range(N):
    neighbors_count = random.randint(0, max_neighbors)
    for _ in range(neighbors_count):
        # Losowo wybieramy inny lek jako zamiennik
        substitute = random.choice(drugs)
        if substitute != drugs[i]:
            # Dodajemy lek i jego zamiennik
            # Zakładam, że add_drug z parametrem 'substitutes' robi odpowiednie wpisy w reverse_substitutes,
            # więc musimy ręcznie to zaktualizować — lub inaczej:
            # Możesz dodać lek z listą zamienników przy tworzeniu, ale tutaj symulujemy aktualizację po fakcie.
            # W twojej implementacji musisz mieć funkcję do dodawania zamienników (jeśli nie, to test możesz uprościć).
            # Tutaj zakładam, że możesz wprost aktualizować reverse_substitutes:
            db.reverse_substitutes.setdefault(substitute, []).append(drugs[i])

print("Start testu wyszukiwania najlepszych zamienników...")

start_time = time.time()

# Wykonujemy wyszukiwanie najlepszych zamienników na kilku lekach
for i in range(50):  # 50 zapytań BFS
    idx = random.randint(0, N-1)
    drug_id = drugs[idx]
    best = db.find_best_alternative(drug_id, max_steps=2)
    print(f"Najlepszy zamiennik dla {drug_id} to {best}")

end_time = time.time()
elapsed = end_time - start_time

print(f"Czas wykonania 50 wyszukiwań find_best_alternative (max_steps=2): {elapsed:.2f} sekund")
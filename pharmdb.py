# Duży projekt zaliczeniowy z ASD 2025
# PharmDB – system zarządzania i analizy leków
# Autor rozwiązania: Mateusz Roman

import heapq
from collections import deque

class Drug:
    def __init__(self, drug_id, name, insert_order, indications=None, substitutes=None, side_effects=None):
        self.id = drug_id
        self.name = name
        self.indications = {}                   # wskazania w leczeniu (choroba, skuteczność)
        self.efficacy_histogram = [0]*11        # indeksy 1-10

        if indications:
            for disease, efficacy in indications:
                self.indications[disease] = efficacy

                # Aktualizuj histogram wskazań: liczba wskazań z efektywnością
                for level in range(1, efficacy+1):
                        self.efficacy_histogram[level] += 1      

        if substitutes:
            self.substitutes = set(substitutes) # leki, które ten lek może zastąpić
        else:
            self.substitutes = set()
        self.replaced_by = set()                # leki, które mogą zastąpić ten lek (odwrotna relacja)

        if side_effects:                        # efekty działań nieporządanych (poziom dolegliwości, częstotliwość)
            self.side_effects = side_effects
        else:
            self.side_effects = []

        # Oblicz raz przy dodawaniu wartości (aby potem drugi raz tego nie liczyć)
        self.risk_score = self._compute_risk_score()
        self.worst_effect_name = self._compute_worst_effect_name()

        # Kolejność dodania do bazy (potrzebna przy remisach)
        self.insert_order = insert_order

    def _compute_risk_score(self):
        score = 0.0
        for _, level, freq in self.side_effects:
            score += level * freq
        return score

    def _compute_worst_effect_name(self):
        if not self.side_effects:
            return None
        # Szukaj najpierw najwyższego poziomu dolegliwości
        max_level = 0
        for effect in self.side_effects:
            if effect[1] > max_level:
                max_level = effect[1]

        # Przeszukuj efekty o tym poziomie, szukam tego o największej częstości
        worst_effect = None
        worst_frequency = 0
        for effect in self.side_effects:
            if effect[1] == max_level:
                if effect[2] > worst_frequency:
                    worst_frequency = effect[2]
                    worst_effect = effect

        return worst_effect[0] if worst_effect else None



class PharmDB:
    '''
        Klasa przechowująca kompleksową bazę danych leków oraz umożliwiająca analizę ich wzajemnych zależności.
        System zapewnia efektywne odpowiedzi na zapytania dotyczące bezpieczeństwa przyjmowanych leków 
        i optymalizacji ich doboru.

        Kazdy lek jest opisany następującymi atrybutami:
            - id: unikalny identyfikator nadawany przez system (np. "D0001", "D0002")
            - name: unikalna nazwa leku (np. "Apap", "Ibuprom")
            - indications: lista wskazań terapeutycznych (chorób) wraz z poziomem skuteczności (skala 1-10)
            - substitutes: lista leków, które mogą być zastąpione przez dany lek
                    (jeśli lek A ma na liście substitutes lek B, oznacza to, że B może być zastąpiony przez A)
            - side_effects: lista działań niepożądanych (nazwa objawu, poziom dolegliwości 1-3, częstotliwość)
    '''

    def __init__(self):
        # Słownik leków po identyfikatorze
        self.drugs_by_id = {}

        # Relacje odwrotna zamienników jako graf
        self.reverse_substitutes = {}      # B → zbiór A

        # Choroba → (efektywność, ID najnowszego leku)
        self.best_drug_for_disease = {}

        # Choroba → kopiec leków (efektywność, -kolejność, ID), do szybkiej aktualizacji najlepszego
        self.indication_heap = {}

        # Numer Generatora ID (numerowany jako D0001, D0002, itd.)
        # Potrzebny jest do rozstrzygania remisów (im większy, tym lek później dodany)
        self.next_id_number = 1


    def add_drug(self, drug_name, indications=None, substitutes=None, side_effects=None):
        '''
            Dodaje nowy lek do bazy danych o podanych wskazaniach terapeutycznych, 
            lekach zastępowanych i efektach ubocznych.
            
            Args:
               drug_name (str): nazwa leku
               indications (list, optional): lista krotek (choroba, skuteczność)
               substitutes (list, optional): lista identyfikatorów leków, które mogą być zastąpione przez nowy lek
               side_effects (list, optional): lista krotek (objaw, poziom dolegliwości, częstotliwość)
            
            Returns:
               str: identyfikator dodanego leku
            
            Wymagana złożoność czasowa: O(k log K + s + e), gdzie:
               - k to liczba wskazań terapeutycznych
               - K to maksymalna liczba leków dla dowolnego wskazania terapeutycznego
               - s to liczba zamienników
               - e to liczba działań niepożądanych
        '''

        # Generowanie ID
        drug_id = f"D{self.next_id_number:04d}"

        # Stwórz obiekt Drug
        drug = Drug(
            drug_id=drug_id,
            name=drug_name,
            insert_order=self.next_id_number,
            indications=indications,
            substitutes=substitutes,
            side_effects=side_effects
        )

        # Zwiększ licznik dodanych leków
        self.next_id_number += 1

        # Dodaj lek do słownika leków
        self.drugs_by_id[drug_id] = drug

        for sub_id in drug.substitutes:
            # Z warunków zadania musi być id już w bazie, ale wypada dodać sprawdzenie
            if sub_id in self.drugs_by_id:
                # Zaktualizuj odwrotną relację
                if sub_id not in self.reverse_substitutes:
                    self.reverse_substitutes[sub_id] = set()
                self.reverse_substitutes[sub_id].add(drug_id)
                # Zaktualizuj także obiekt zamienianego leku
                self.drugs_by_id[sub_id].replaced_by.add(drug_id)
            else:
                raise Exception("Dodany lek może być zamiennikiem tylko dla leków wcześniej dodanych do bazy danych!")

        # Aktualizuj struktury dotyczące wskazań
        if indications:
            for disease, efficacy in indications:
                # Kopiec dla choroby
                if disease not in self.indication_heap:
                    self.indication_heap[disease] = []
                # Dodaj z minusami, bo heapq to kopiec minimalny — symuluj działanie kopca maksymalnego
                heapq.heappush(self.indication_heap[disease], (-efficacy, -drug.insert_order, drug_id))

                # Aktualizuj najlepszy lek
                if disease not in self.best_drug_for_disease:
                    self.best_drug_for_disease[disease] = (efficacy, drug_id)
                else:
                    best_efficacy, best_id = self.best_drug_for_disease[disease]
                    if (efficacy > best_efficacy) or (efficacy == best_efficacy and drug.insert_order > self.drugs_by_id[best_id].insert_order):
                        self.best_drug_for_disease[disease] = (efficacy, drug_id)

        return drug_id


    def number_of_indications(self, drug_id, min_efficacy):
        '''
            Zwraca liczbę wskazań terapeutycznych o efektywności co najmniej min_efficacy dla podanego leku.

            Args:
                drug_id (str): identyfikator leku
                min_efficacy (int): minimalna wymagana efektywność

            Returns:
                int: liczba wskazań terapeutycznych spełniających kryterium
        
            Wymagana złożoność czasowa: O(1)
        '''
        
        drug = self.drugs_by_id.get(drug_id)
        if not drug:
            return 0
        return drug.efficacy_histogram[min_efficacy]



    def number_of_alternative_drugs(self, drug_id):
        '''
            Zwraca liczbę leków, które mogą bezpośrednio zastąpić dany lek.
            
            Args:
                drug_id (str): identyfikator leku
            
            Returns:
                int: liczba leków mogących zastąpić dany lek
            
            Wymagana złożoność czasowa: O(1)
        '''
        drug = self.drugs_by_id.get(drug_id)
        if not drug:
            return 0
        return len(drug.replaced_by)


    def worst_side_effect(self, drug_id):
        '''
            Zwraca nazwę najbardziej dotkliwego skutku ubocznego dla podanego leku.
            Najbardziej dotkliwy to skutek o największej częstotliwości spośród tych o największym poziomie dolegliwości.
        
            Args:
            drug_id (str): identyfikator leku
        
            Returns:
            str: nazwa najbardziej dotkliwego skutku ubocznego lub None jeśli lek nie ma skutków ubocznych
        
            Wymagana złożoność czasowa: O(1)
        '''
       
        drug = self.drugs_by_id.get(drug_id)
        if not drug:
            return None
        return drug.worst_effect_name


    def risk_score(self, drug_id):
        '''
            Zwraca wskaźnik ryzyka (risk score) zdefiniowany jako ważona suma wszystkich działań niepożądanych leku.
            Risk score = suma(częstość występowania x poziom dolegliwości) po wszystkich efektach ubocznych.

            Args:
                drug_id (str): identyfikator leku

            Returns:
                float: wskaźnik ryzyka
        
            Wymagana złożoność czasowa: O(1)
        '''
        drug = self.drugs_by_id.get(drug_id)
        if not drug:
            return 0.0
        return drug.risk_score


    def find_best_alternative(self, drug_id, max_steps=2):
        '''
            Zwraca identyfikator leku o minimalnym ryzyku spośród leków, które można zastosować 
            zamiast leku drug_id przy ograniczeniu liczby zamian (max_steps).
            
            Args:
            drug_id (str): identyfikator leku
            max_steps (int, optional): maksymalna liczba zamian, domyślnie 2
            
            Returns:
                str: identyfikator leku o minimalnym ryzyku
            
            Wymagana złożoność czasowa: funkcja powinna działać istotnie szybciej niż O(D+S)
        '''

        if drug_id not in self.drugs_by_id:
            return None

        # BFS (lek_id, liczba wykonanych kroków)
        visited = set()
        queue = deque([(drug_id, 0)])
        visited.add(drug_id)

        best_id = drug_id
        best_score = self.drugs_by_id[drug_id].risk_score

        while queue:
            current_id, steps = queue.popleft()
            current_score = self.drugs_by_id[current_id].risk_score

            # Aktualizuj najlepszy lek
            if (current_score < best_score) or (current_score == best_score and current_id < best_id):
                best_score = current_score
                best_id = current_id

            # Przejdź do sąsiadów, jeśli nie przekroczono max_steps
            if steps < max_steps:
                for neighbor in self.reverse_substitutes.get(current_id, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, steps + 1))

        return best_id


    def longest_alternative_list(self):
        '''
            Zwraca listę identyfikatorów leków stanowiącą najdłuższy ciąg zamienników leków,
            gdzie każdy kolejny lek na liście może bezpośrednio zamienić lek poprzedni.
        
            Przykład: jeśli A może być zastąpione przez B, B przez C lub D, a C przez D,
            to wynikiem działania tej funkcji powinna być lista [id(A), id(B), id(C), id(D)].
        
            Returns:
                list: lista identyfikatorów leków

            Wymagana złożoność czasowa: O(d), gdzie d to długość zwracanej listy
        '''
        memo = {}  # drug_id: (length, next_drug_id or None)

        def dfs(drug_id):
            if drug_id in memo:
                return memo[drug_id]

            max_length = 1
            next_drug = None
            # Przejdź po liście sąsiadów, jeżeli nie ma to zwróć pustą listę
            for neighbor in self.reverse_substitutes.get(drug_id, []):
                length, _ = dfs(neighbor)
                if length + 1 > max_length:
                    max_length = length + 1
                    next_drug = neighbor
                # Porównaj lek po id w przypadku remisu długości
                elif length + 1 == max_length and neighbor < next_drug:
                    next_drug = neighbor

            memo[drug_id] = (max_length, next_drug)
            return memo[drug_id]

        # Znajdź najlepszy start
        best_start = None
        best_length = 0

        for drug_id in self.drugs_by_id:
            length, _ = dfs(drug_id)
            if length > best_length:
                best_length = length
                best_start = drug_id
            elif length == best_length and drug_id < best_start:
                best_start = drug_id

        # Odtwórz ścieżkę z memo
        path = []
        current = best_start
        while current:
            path.append(current)
            _, nxt = memo[current]
            current = nxt

        return path


    def find_best_drug_for_indication(self, disease_name):
        '''
            Zwraca identyfikator leku o największej efektywności dla wskazanej choroby.
            W przypadku wielu leków o takiej samej efektywności, zwraca najpóźniej dodany do bazy.

            Args:
                disease_name (str): nazwa choroby

            Returns:
                str: identyfikator leku o największej efektywności
        
            Wymagana złożoność czasowa: O(1)
        '''
        if disease_name not in self.best_drug_for_disease:
            return None
        return self.best_drug_for_disease[disease_name][1]  # (efficacy, drug_id)


    def update_best_indication(self, disease_name, new_efficacy):
        '''
            Zmienia efektywność najlepszego leku dla wskazanej choroby, tj.
            leku, który jest wynikiem działania find_best_drug_for_indication
        
            Args:
                disease_name (str): nazwa choroby
                new_efficacy (int): nowa efektywność
        
            Wymagana złożoność czasowa: O(log K)
        '''
        if disease_name not in self.best_drug_for_disease:
            return

        _, drug_id = self.best_drug_for_disease[disease_name]
        drug = self.drugs_by_id[drug_id]

        # Aktualizuj dane w obiekcie
        drug.indications[disease_name] = new_efficacy

        # Wrzuć nowy wpis do kopca
        heapq.heappush(self.indication_heap[disease_name], (-new_efficacy, -drug.insert_order, drug_id))

        # Oczyść kopiec z przeterminowanych wpisów
        while self.indication_heap[disease_name]:
            eff, neg_order, top_id = self.indication_heap[disease_name][0]
            top_drug = self.drugs_by_id[top_id]
            current_eff = top_drug.indications.get(disease_name, None)
            if current_eff is not None and -eff == current_eff:
                self.best_drug_for_disease[disease_name] = (current_eff, top_id)
                break
            else:
                heapq.heappop(self.indication_heap[disease_name])
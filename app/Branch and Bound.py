import copy
import numpy as np

class Node:
    '''
    Klasa tworząca wierzchołki
    '''

    def __init__(self, parents=[], node_cost=0, index=0, checked=False):
        self.parents = parents  # lista rodziców wierzchołka
        self.node_cost = node_cost  # koszt przejścia od początku drogi do wierzchołka
        self.index = index  # indeks wierzchołka
        self.children = []  # lista dzieci wierzchołka
        self.checked = checked  # stan sprawdzenia - odwiedzenia
        self.matrix = []  # macierz danego wierzchołka

    def __str__(self):
        '''
        Pomocnicze przeciążenie wyśiwetlające dane o konkretnym wierzchołku
        :return:
        '''
        return ("Wierzcholek: {}\nKoszt: {}\nDzieci: {}\nRodzice: {}\nMatrix: {}\n\n".format(self.index, self.node_cost,
                                                                                             self.children,
                                                                                             self.parents, self.matrix))

class read_data:
    '''
    READ_DATA
    -wczytuje dane z pliku
    -wykonuje algorytmy
    -przechwouje dane
    -zwraca wyniki
    '''

    def __init__(self, matrix, size):
        self.matrix = matrix  # wczytywana macierz
        self.size = size  # ilość miast, wielkość macierzy
        self.startingPoint = 0  # ustawienie punktu startowego, początku drogi
        self.nodes_list = []  # lista przechowująca wierzhołki
        self.min = 999999999  # minimalny koszt - nadpisywany
        self.path = []  # aktualna droga
        self.min_path = []  # minimalna droga
        self.iterations = 0  # liczba wywolan funkcji
        self.sec_min = 0

    def prep_data(self):
        '''
        Przygotowanie danych
        '''

        self.matrix_with_minuses = self.change_zero(copy.deepcopy(self.matrix))  # zmiana przekątnej z 0 na -1
        self.main_cost, self.reduced_matrix = self.compute_brand(
            self.matrix_with_minuses)  # zredukowana macierz i koszt minimalny

    def change_zero(self, mat):
        '''
        zmienienie 0 na -1 w określonej macierzy
        :param mat:
        :return:
        '''
        for i in range(0, self.size):
            for j in range(0, self.size):
                if i == j:
                    mat[i][j] = -1
        return mat

    def print_nicely(self, mat):
        '''
        Wyświetlenie macierzy z wyszególnieniem na wierzchołki
        :param mat - macierz do wyświetlenia:
        :return:
        '''
        size = len(mat)
        row = '  |  '
        dash = '---'
        for i in range(0, size):
            row += str(i)
            row += '   '
            dash += "----"

        print(row)
        print(dash)

        for i in range(0, size):
            help_list = mat[i]
            print("{} | {}".format(i, help_list))

    def matrix_inf(self, mat, v1, v2):
        '''
        Dla przejścia z v1 do v2, zaznaczenie calego wybranego wiersza i kolumny na wartości -1
        zaznaczenie wartościa -1 miejsce powrotu z v2 do v1
        :param mat: macierz
        :param v1: wierzchołek pierwszy - wiersz
        :param v2: wierzchołek drugi - kolumna
        :return:
        '''
        size = len(mat)
        for i in range(0, size):
            for j in range(0, size):
                if i == v1 or j == v2:
                    mat[i][j] = -1
        mat[v2][v1] = -1
        return mat

    def compute_brand(self, mat):
        min = 9999999
        reduced = 0
        # redukcja po wierszach, wyszukanie wartości minimalnej, odjęcie jej od każdej wartości, dodanie jej do kosztu redukcji
        for i in range(0, self.size):
            for j in range(0, self.size):
                if mat[i][j] < min and mat[i][j] != -1:
                    min = mat[i][j]
            if min != 9999999:
                reduced += min
            for k in range(0, self.size):
                if mat[i][k] != -1:
                    mat[i][k] -= min
            min = 9999999

        # redukcja po kolumnach, wyszukanie wartości minimalnej, odjęcie jej od każdej wartości, dodanie jej do kosztu redukcji
        for i in range(0, self.size):
            for j in range(0, self.size):
                if mat[j][i] < min and mat[j][i] != -1:
                    min = mat[j][i]
            if min != 9999999:
                reduced += min
            for k in range(0, self.size):
                if mat[k][i] != -1:
                    mat[k][i] -= min
            min = 9999999

        return reduced, mat  # zwrócenie zredukowanej macierzy i kosztu redukcji

    def calculate_cost_from_verts(self, v1, v2, mat):
        '''
        Wyliczenie kosztu przejscia miedzy dwoma miastami
        :param v1: wierzchołek 1
        :param v2: wierzchołek 2
        :param mat: macierz
        :return:
        '''
        edge = mat[v1][v2]  # pobranie krawędzi miedzy miastami, zapisanie kosztu
        help_matrix = copy.deepcopy(mat)  # macierz pomocnicza
        help_matrix = self.matrix_inf(help_matrix, v1, v2)  # zaznaczenie kolumny i wiersza na -1
        cost, help_matrix = self.compute_brand(
            help_matrix)  # wyliczenie kosztu redukcji macierzy i zwrócenie macierzy zredukowanej
        whole_cost = cost + edge  # zliczenie całkowitego kosztu
        return whole_cost, help_matrix  # zwrócenie kosztu i macierzy

    def bb(self, current_node):
        '''
        Branch&Bound
        :param current_node:
        :return:
        '''
        self.iterations += 1  # zwiększenie liczby wywołań metody
        if current_node in self.nodes_list:  # jeżeli wierzchołek już znajdował się na liście
            for node in self.nodes_list:
                if node == current_node:
                    node.checked = True  # wierzchołek odwiedzony
        else:  # jeżeli wierzchołek nie znajdował się na liście
            current_node.checked = True  # wierzchołek odwiedzony
            self.nodes_list.append(current_node)  # dodanie wierzchołka do listy

        # generowanie dzieci
        parents_list = copy.deepcopy(current_node.parents)  # kopia wierzchołków rodziców
        parents_list.append(current_node.index)  # dodanie aktualnego wierzchołka
        if len(current_node.children) != 0:  # jeżeli nie koniec gałęzi
            for child in current_node.children:  # dla każdego pozostałego dziecka
                current_matrix = copy.deepcopy(current_node.matrix)  # kopia macierzy aktualnego wierzchołka
                child_list = []  # stworzenie listy dzieci aktualnego wierzchołka
                for i in range(0, self.size):  # wyszukwanie dzieci
                    if child == i or i in parents_list:  # dodanie dzieci poza sobą
                        continue
                    else:
                        child_list.append(i)

                # wyliczenie kosztu przejścia do tworzonego wierzchołka i macierzy dla niego
                cost, node_matrix = self.calculate_cost_from_verts(current_node.index, child, current_matrix)
                cost += current_node.node_cost  # zliczenie kosztu całkowitego kosztu
                my_node = Node(parents_list, cost, child)  # tworzenie nowego wierzchołka
                my_node.children = child_list  # przypisywanie wartości
                my_node.matrix = node_matrix  # przypisywanie wartości
                self.nodes_list.append(my_node)  # dodanie utworzonego wierzchołka do listy

            min = 9999999  # koszt minimalny
            for position, node in enumerate(self.nodes_list):
                if node.node_cost < min and node.checked == False:  # jeżeli koszt wierzchołka znalezionego mniejszy niż poprzedni
                    min = node.node_cost  # zmiana kosztu minimalnego
                    node_position = position  # zapisanie pozycji w liście
                    self.min = min

            next_node = self.nodes_list[node_position]  # wybranie następnego wierzchołka, z najniższym kosztem

            min = 9999999  # koszt minimalny
            for position, node in enumerate(self.nodes_list):
                if node.node_cost > self.min and node.node_cost < min and node.checked == False:  # jeżeli koszt wierzchołka znalezionego mniejszy niż poprzedni
                    min = node.node_cost  # zmiana kosztu minimalnego
                    self.sec_min = min  # ustawienie drugiego minimalnego kosztu

            for pos, node in enumerate(self.nodes_list):
                if node.node_cost != self.min and node.node_cost != self.sec_min:
                    self.nodes_list.pop(pos)

            print(next_node)
            self.bb(next_node)  # wywołanie metody dla następnego wierzchołka

    def init_first_node(self):
        '''
        Stowrzenie pierwszego wierzchołka dla miasta początkowego
        :return:
        '''
        parents = []  # wierzchołek nie ma rodziców
        first_node_matrix = copy.deepcopy(self.reduced_matrix)  # macierzy dla wierzchołka
        first_node = Node(parents, self.main_cost, self.startingPoint, True)  # stworzenie obiektu
        first_node.matrix = first_node_matrix  # przypisanie macierzy
        children_list = []  # stowrzenie listy dla dzieci
        for i in range(0, self.size):
            if i != self.startingPoint:
                children_list.append(i)  # wypełnienie listy dzieci
        first_node.children = children_list  # przypisanie listy dzieci
        return first_node  # zwrócenie wierzchołka początkowego

    def doBranchAndBound(self):
        first_node = self.init_first_node()  # stworzenie pierwszego wierzchołka dla branch&bound
        print(first_node)
        self.bb(first_node)  # wykonanie branch&bound


# def changeZeroToInf(matrix): # change zeros to inf
#     result = np.where(matrix == 0, np.inf, matrix)
#     return result
#
#
# def findMinAndSubstract(matrix, type='row'):
#     i = 0
#     result = []
#     if type == 'column':
#         matrix = matrix.T
#     minimums = matrix.min(axis=1)
#     for row in matrix:
#         row = row - minimums[i]
#         i = i + 1
#         result.append(row)
#     fin_result = np.array(result)
#     if type == 'column':
#         fin_result = fin_result.T
#     return fin_result, minimums
#
#
#
#
# mat = np.array([[0, 20, 30, 31, 28, 40],
#                 [30, 0, 10, 14, 20, 44],
#                 [40, 20, 0, 10, 22, 50],
#                 [41, 24, 20, 0, 14, 42],
#                 [38, 30, 32, 24, 0, 28],
#                 [50, 54, 60, 52, 38, 0]])
#
# costs = mat
#
# size = 6
# print(mat)
# mat = changeZeroToInf(mat)
# result, elements_sum = findMinAndSubstract(mat, 'column')
# print(result)


matrix = [[0, 20, 30, 31, 28, 40],
            [40, 0, 20, 10, 22, 50],
            [30, 10, 0, 14, 20, 44],
            [41, 24, 20, 0, 14, 42],
            [38, 30, 32, 24, 0, 28],
            [50, 54, 60, 52, 38, 0]]

size = 6

data = read_data(matrix, size)
data.prep_data()
data.print_nicely(matrix)
data.doBranchAndBound()

print(data.min)

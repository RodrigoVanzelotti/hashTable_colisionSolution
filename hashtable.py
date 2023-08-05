import csv

class Player:
    def __init__(self, sofifa_id, name, player_positions):
        self.sofifa_id = sofifa_id
        self.name = name
        self.player_positions = player_positions
        self.next = None

class HashTable:
    def __init__(self, M):
        self.M = M
        self.table = [None] * M

    def hash_func(self, key):
        return key % self.M

    def insert(self, player):
        index = self.hash_func(player.sofifa_id)
        if not self.table[index]:
            self.table[index] = player
        else:
            current = self.table[index]
            while current.next:
                current = current.next
            current.next = player

    def search(self, key):
        index = self.hash_func(key)
        current = self.table[index]
        tests = 1
        while current:
            if current.sofifa_id == key:
                return current, tests
            current = current.next
            tests += 1
        return None, tests
    
    # Função para calcular as estatísticas da tabela hash
    def calculate_table_stats(self):
        num_entries = 0
        min_list_size = float('inf')
        max_list_size = 0
        total_list_size = 0

        for slot in self.table:
            current = slot
            list_size = 0
            while current:
                num_entries += 1
                list_size += 1
                current = current.next
            if list_size > 0:
                min_list_size = min(min_list_size, list_size)
                max_list_size = max(max_list_size, list_size)
                total_list_size += list_size

        average_list_size = total_list_size / num_entries if num_entries > 0 else 0

        return num_entries, min_list_size, max_list_size, average_list_size

    
def parse_players(file_path):
    players = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sofifa_id = int(row['sofifa_id'])
            name = row['name']
            player_positions = row['player_positions']
            player = Player(sofifa_id, name, player_positions)
            players.append(player)
    return players

def read_queries(file_path):
    queries = []
    with open(file_path, 'r', encoding='utf-8') as queryfile:
        for line in queryfile:
            queries.append(line.strip())
    return queries

def run_experiment(M, players_file, queries_file, output_file):
    # Crie a tabela hash com o tamanho M
    hash_table = HashTable(M)

    # Leia os jogadores do arquivo CSV e insira na tabela hash
    players = parse_players(players_file)
    for player in players:
        hash_table.insert(player)

    # Leia as consultas do arquivo
    queries = read_queries(queries_file)

    # Realize as consultas e calcule as estatísticas
    total_tests = 0
    min_tests = float('inf')
    max_tests = 0
    num_found = 0
    found_tests = []

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Estatísticas da tabela hash
        num_entries, min_list_size, max_list_size, avg_list_size = hash_table.calculate_table_stats()
        empty_entries = M - num_entries

        outfile.write("PARTE1: ESTATISTICAS DA TABELA HASH\n")
        outfile.write(f"NUMERO DE ENTRADAS DA TABELA USADAS: {num_entries}\n")
        outfile.write(f"NUMERO DE ENTRADAS DA TABELA VAZIAS: {empty_entries}\n")
        outfile.write(f"TAXA DE OCUPAÇÃO: {num_entries/M:.2f}\n")
        outfile.write(f"MINIMO TAMANHO DE LISTA: {min_list_size}\n")
        outfile.write(f"MAXIMO TAMANHO DE LISTA: {max_list_size}\n")
        outfile.write(f"MEDIO TAMANHO DE LISTA: {avg_list_size:.2f}\n\n")

        # Realize as consultas e calcule as estatísticas
        for query in queries:
            result, tests = hash_table.search(int(query))
            if result:
                outfile.write(f"ID: {result.sofifa_id}, NAME: {result.name}, POSITION: {result.player_positions}, TESTES:{tests}\n")
                total_tests += tests
                min_tests = min(min_tests, tests)
                max_tests = max(max_tests, tests)
                num_found += 1
                found_tests.append(tests)
            else:
                outfile.write(f"ID: {query}, MISS, TESTES: {tests}\n")

        avg_tests = total_tests / len(queries) if len(queries) > 0 else 0

        # Estatísticas das consultas
        outfile.write("\nPARTE2: ESTATISTICAS DAS CONSULTAS\n")
        outfile.write(f"TOTAL DE CONSULTAS REALIZADAS: {len(queries)}\n")
        outfile.write(f"TOTAL DE CONSULTAS COM MATCH: {num_found}\n")
        outfile.write(f"MINIMO NUMERO DE TESTES POR NOME ENCONTRADO: {min_tests if min_tests != float('inf') else 0}\n")
        outfile.write(f"MAXIMO NUMERO DE TESTES POR NOME ENCONTRADO: {max_tests}\n")
        outfile.write(f"MEDIA NUMERO DE TESTES NOME ENCONTRADO: {avg_tests:.2f}\n")

        # Extra: Caso queira calcular o desvio padrão dos testes para nomes encontrados
        if num_found > 0:
            variance = sum((test - avg_tests) ** 2 for test in found_tests) / num_found
            std_deviation = variance ** 0.5
            outfile.write(f"DESVIO PADRÃO DO NUMERO DE TESTES NOME ENCONTRADO: {std_deviation:.2f}\n")

# Exemplo de uso:
if __name__ == "__main__":
    M_values = [1000, 2000, 4000, 8000]
    players_file = "players.csv"
    queries_file = "consultas-fifa.txt"

    for M in M_values:
        output_file = f"experimento{M}.txt"
        run_experiment(M, players_file, queries_file, output_file)
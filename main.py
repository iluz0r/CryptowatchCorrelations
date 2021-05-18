import itertools
from datetime import datetime

from numpy import zeros, unravel_index


def find_max_indices(corr_mat, num_max_to_find):
    # Appiattisco la matrice in un unico vettore
    corr_mat_flatten = corr_mat.flatten()
    # Cerca gli indici (nell'array rappresentante la matrice) dei valori massimi
    max_indices_flatten = (-corr_mat_flatten).argsort()[:num_max_to_find]
    # Trasforma gli indici del vettore 1D in indici per la matrice 2D
    max_indices = unravel_index(max_indices_flatten, corr_mat.shape)
    return max_indices


def create_corr_mat(lines, coins):
    # Inizializza la matrice di correlazione a 0
    corr_mat = zeros((len(coins), len(coins)))
    # Trova le righe della matrice di correlazione nel seguente formato
    # coin (col_0)
    # val (col_1)
    # val (col_2)
    # ...
    row = col = 0
    for line in lines[len(coins) + 2:]:
        if line in coins:
            row = coins.index(line)
            col = 0
        elif not (line == '-'):
            corr_mat[row][col] = float(line)
            col += 1
        else:
            col += 1
    return corr_mat


def create_coins_list(lines):
    coins = []
    for line in lines:
        if not (line.startswith(".") or line.startswith("-") or line == ''):
            if line not in coins:
                coins.append(line)
    return coins


def read_file_as_list(file_name):
    # Legge il file e lo salva in una lista (ogni riga è un elemento della lista)
    lines = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
    lines = [elem.strip() for elem in lines]
    return lines


# 17.32 ('DASH', 'BAT', 'BNB', 'VET', 'NEO')
# 25.869999999999997 ('BTC', 'DASH', 'BAT', 'BNB', 'VET', 'NEO')
# NEO DASH BAT ONT BNB BTC VET SC ETH QTUM ZIL TRX LTC LINK XMR
def main():
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    lines_24h = read_file_as_list("24h.txt")
    lines_7d = read_file_as_list("7d.txt")
    # Crea la lista delle coins
    coins = create_coins_list(lines_24h)
    # Crea la matrice di correlazione
    corr_mat_24h = create_corr_mat(lines_24h, coins)
    corr_mat_7d = create_corr_mat(lines_7d, coins)
    corr_mat = corr_mat_24h + corr_mat_7d
    # Cerca gli indici dei valori massimi
    num_max_to_find = 80
    max_indices = find_max_indices(corr_mat.copy(), num_max_to_find)
    max_indices_rows = max_indices[0]
    max_indices_cols = max_indices[1]
    for i in range(0, num_max_to_find):
        couple = coins[max_indices_rows[i]] + coins[max_indices_cols[i]]
        corr_value = corr_mat[max_indices_rows[i], max_indices_cols[i]]
        print("{couple}: {corr_value}".format(couple=couple, corr_value=corr_value))

    # Effettua combinazioni su n (in questo caso 6) posti di tutte le coins in lista. Per ognuno di questi subset,
    # effettua tutte le combinazioni su 2 posti e calcola la correlazione complessiva delle coppie. Infine, calcola il
    # subset da n (in questo caso da 6) coins con il valore massimo di correlazione
    """max_corr_subset = None
    max_corr_sum = 0
    for elem in itertools.combinations(coins, 6):
        corr_sum = 0
        for couple in itertools.combinations(elem, 2):
            coin_row = couple[0]
            coin_col = couple[1]
            row = coins.index(coin_row)
            col = coins.index(coin_col)
            if col > row:
                tmp = row
                row = col
                col = tmp
            corr_sum += corr_mat[row][col]
        if corr_sum > max_corr_sum:
            max_corr_sum = corr_sum
            max_corr_subset = elem
    print(max_corr_sum, max_corr_subset)"""

    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))


if __name__ == '__main__':
    main()

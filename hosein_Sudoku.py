import time
from typing import Optional, Tuple, List, Set


class Sudoku:
    def __init__(self, table: Optional[Tuple[Tuple[int, ...], ...]] = None):
        self.row_allow: List[Set[int], ...] = []
        self.column_allow: List[Set[int], ...] = []
        self.box_allow: List[List[Set[int], ...], ...] = []
        if table:
            self.raw_table = table
            self.table = [list(row) for row in table]
        else:
            self._get_table()
        self.analysis()
        self.guess_list: List[Tuple[int, int, int], ...] = []
        self.guess_do: List[List[List]] = []

    def __str__(self):
        rows = [''.join(map(str, row)) for row in self.table]
        return '\n'.join(rows)

    def _get_table(self):
        table = []
        for _ in range(9):
            while True:
                try:
                    line = input().replace(' ', '')
                    if line.isalnum() and len(line) == 9:
                        table.append(list(map(int, line)))
                    else:
                        raise UserWarning
                except UserWarning:
                    print('Please enter the numbers correctly:\nEnter 0 for empty cell')
                else:
                    break
        self.table = table
        self.raw_table = tuple(table)

    def possibility(self, node_row, node_column):
        if self.table[node_row][node_column]:
            return 0
        else:
            return self.row_allow[node_row] & self.column_allow[node_column] & self.box_allow[node_row // 3][
                node_column // 3]

    def analysis(self):
        num_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.row_allow = [num_set.copy() for _ in range(9)]
        self.column_allow = [num_set.copy() for _ in range(9)]
        self.box_allow = [[num_set.copy() for _ in range(3)] for _ in range(3)]
        for n, row in enumerate(self.table):
            self.row_allow[n] -= set(row)
            for k in range(3):
                self.box_allow[n // 3][k] -= set(row[3 * k:3 * (k + 1)])
            for m, clm in enumerate(row):
                self.column_allow[m] -= {clm}

    def solve(self):
        some_done = True
        while some_done:
            some_done = self.num_from_cell_possibility() or self.single_num_extract_from_constrains()
        else:
            if any(0 in row for row in self.table):
                try:
                    self.decision()
                    self.solve()
                except UserWarning:
                    self.decision_rollback()
                    self.solve()

    def num_from_cell_possibility(self, try_guess: Optional[List[List]] = None):
        do_any = False
        for n_cell in range(9):
            for m_cell in range(9):
                data_set = self.possibility(n_cell, m_cell)
                if data_set:
                    if len(data_set) == 1:
                        do_any = True
                        cell = n_cell, m_cell, data_set.pop()
                        self.write_cell(*cell)
                        if try_guess:
                            try_guess[-1].append(cell)
                    elif len(data_set) == 0 and try_guess:
                        raise UserWarning(1)
        return do_any

    def num_guess(self):
        for n_cell in range(9):
            for m_cell in range(9):
                data_set = self.possibility(n_cell, m_cell)
                if data_set:
                    if len(data_set) == 2:
                        cell = n_cell, m_cell, data_set.pop()
                        self.write_cell(*cell)
                        self.guess_list.append(cell)
                        return None
        raise UserWarning(2)

    def write_cell(self, n_cell, m_cell, num):
        self.row_allow[n_cell] -= {num}
        self.column_allow[m_cell] -= {num}
        self.box_allow[n_cell // 3][m_cell // 3] -= {num}
        self.table[n_cell][m_cell] = num

    def single_num_extract_from_constrains(self):
        do_any = False
        for n_cell in range(9):
            for m_cell in range(9):
                data_set = self.possibility(n_cell, m_cell)
                if data_set:
                    m_data_set = data_set.copy()
                    n_data_set = data_set.copy()
                    b_data_set = data_set.copy()
                    for mm in range(9):
                        m_node = self.possibility(n_cell, mm)
                        if mm != m_cell and m_node:
                            m_data_set -= m_node
                    for nn in range(9):
                        n_node = self.possibility(nn, m_cell)
                        if nn != n_cell and n_node:
                            n_data_set -= n_node
                    for nn in range(9):
                        for mm in range(9):
                            if (mm != m_cell or nn != n_cell) and mm // 3 == m_cell // 3 and nn // 3 == n_cell // 3:
                                b_node = self.possibility(nn, mm)
                                if b_node:
                                    b_data_set -= b_node
                    all_data_set = m_data_set | n_data_set | b_data_set
                    if len(all_data_set) == 1:
                        cell = n_cell, m_cell, all_data_set.pop()
                        self.write_cell(*cell)
                        do_any = True
        return do_any

    def decision(self):
        self.guess_do.append(self.table)
        self.num_guess()

    def decision_rollback(self):
        self.table = self.guess_do.pop()
        self.analysis()
        n_cell, m_cell, num = self.guess_list.pop()
        self.row_allow[n_cell] -= {num}
        self.column_allow[m_cell] -= {num}
        self.box_allow[n_cell // 3][m_cell // 3] -= {num}


if __name__ == '__main__':
    base_all_zero = (
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0)
    )

    base_easy = (
        (0, 0, 0, 0, 0, 0, 5, 0, 1),
        (5, 6, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 7, 2, 0, 4, 0, 0, 0),
        (0, 0, 5, 0, 7, 9, 2, 1, 3),
        (0, 0, 4, 1, 0, 2, 0, 5, 9),
        (2, 0, 0, 0, 0, 8, 4, 0, 0),
        (0, 0, 0, 3, 0, 5, 0, 0, 7),
        (8, 0, 1, 0, 2, 6, 9, 3, 4),
        (0, 7, 3, 8, 9, 1, 0, 2, 5)
    )

    base_hard = (
        (0, 0, 4, 0, 0, 3, 5, 6, 8),
        (5, 0, 0, 8, 0, 7, 0, 4, 2),
        (0, 0, 0, 0, 0, 4, 0, 0, 0),
        (8, 0, 5, 0, 1, 2, 0, 0, 0),
        (0, 0, 0, 0, 5, 0, 2, 0, 9),
        (0, 0, 0, 0, 0, 0, 6, 0, 0),
        (0, 7, 8, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0, 5, 0),
        (6, 0, 0, 9, 0, 0, 0, 7, 0)
    )
    base_expert = (
        (3, 0, 0, 9, 0, 0, 0, 0, 0),
        (0, 0, 7, 0, 0, 0, 2, 5, 0),
        (5, 0, 0, 0, 0, 0, 0, 1, 0),
        (0, 0, 0, 1, 0, 2, 0, 7, 9),
        (0, 0, 0, 0, 0, 8, 1, 0, 0),
        (0, 0, 0, 0, 0, 4, 0, 0, 0),
        (0, 7, 0, 0, 0, 0, 0, 0, 0),
        (0, 2, 0, 0, 7, 0, 0, 4, 5),
        (0, 0, 1, 3, 0, 0, 0, 0, 6)
    )
    base_pdf_1 = (
        (5, 3, 0, 0, 7, 0, 0, 0, 0),
        (6, 0, 0, 1, 9, 5, 0, 0, 0),
        (0, 9, 8, 0, 0, 0, 0, 6, 0),
        (8, 0, 0, 0, 6, 0, 0, 0, 3),
        (4, 0, 0, 8, 0, 3, 0, 0, 1),
        (7, 0, 0, 0, 2, 0, 0, 0, 6),
        (0, 6, 0, 0, 0, 0, 2, 8, 0),
        (0, 0, 0, 4, 1, 9, 0, 0, 5),
        (0, 0, 0, 0, 8, 0, 0, 7, 9)
    )
    base_pdf_2 = (
        (3, 0, 6, 5, 0, 8, 4, 0, 0),
        (5, 2, 0, 0, 0, 0, 0, 0, 0),
        (0, 8, 7, 0, 0, 0, 0, 3, 1),
        (0, 0, 3, 0, 1, 0, 0, 8, 0),
        (9, 0, 0, 8, 6, 3, 0, 0, 5),
        (0, 5, 0, 0, 9, 0, 6, 0, 0),
        (1, 3, 0, 0, 0, 0, 2, 5, 0),
        (0, 0, 0, 0, 0, 0, 0, 7, 4),
        (0, 0, 5, 2, 0, 6, 3, 0, 0)
    )
    star_time = time.time()
    sudoku = Sudoku(base_expert)
    sudoku.solve()
    print(sudoku)
    print(time.time() - star_time)

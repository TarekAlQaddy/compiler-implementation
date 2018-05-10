from NonTerminal import NonTerminal
from Terminal import Terminal


def start_parsing(file_name):
    file = open(file_name, 'r')
    file_content = file.read()

    terminal_buffer = ''
    non_terminal_buffer = ''
    lhs_buffer = ''
    is_lhs = False
    is_rhs = False
    is_first_rhs_node = True
    filling_terminal = False
    productions = {}
    terminals = []
    non_terminals = []

    for char in file_content:
        if char == '#':
            is_lhs = True
            is_rhs = False
            is_first_rhs_node = True
            filling_terminal = False
            lhs_buffer = ''
            continue
        if char == '=' and not is_rhs:
            is_lhs = False
            is_rhs = True
            is_first_rhs_node = True
            productions[lhs_buffer] = []
            continue
        if is_lhs:
            if char == ' ':
                continue
            if char.isalnum() or char == '_':
                lhs_buffer += char
                continue
        if is_rhs:
            if char == ' ' or char == '|' or char == '\n':
                if non_terminal_buffer:
                    n = NonTerminal(non_terminal_buffer, None)
                    if is_first_rhs_node:
                        productions[lhs_buffer].append(n)
                    else:
                        length = len(productions[lhs_buffer])
                        temp = productions[lhs_buffer][length - 1]
                        while temp.next:
                            temp = temp.next
                        temp.next = n
                    if char == ' ' or char == '\n':
                        is_first_rhs_node = False
                    elif char == '|':
                        is_first_rhs_node = True
                    non_terminal_buffer = ''
                elif char == '|':
                    is_first_rhs_node = True
                continue
            if char == '\'':
                if terminal_buffer:
                    t = Terminal(terminal_buffer, None)
                    if is_first_rhs_node:
                        productions[lhs_buffer].append(t)
                    else:
                        length = len(productions[lhs_buffer])
                        temp = productions[lhs_buffer][length - 1]
                        while temp.next:
                            temp = temp.next
                        temp.next = t
                    is_first_rhs_node = False
                    filling_terminal = False
                    terminal_buffer = ''
                else:
                    filling_terminal = True
                continue
            if not filling_terminal:
                non_terminal_buffer += char
            elif filling_terminal:
                terminal_buffer += char
    return productions


start_parsing('CFG.txt')

"""
Return Example:
{
    'terminals': [Terminal t1, Terminal t2, ...],
    'non_terminals': [NonTerminal n1, NonTerminal t2, ...],
    'productions': {
        'STATEMENT_LIST': [Node n1, Node n2],
        'METHOD_BODY': [Node n3]
    }
}
"""
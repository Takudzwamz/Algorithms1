import os.path


class Node:
    """description of class"""
    def __init__(self, ch_arc_idx, p_arc):
        self.arcs = {}
        for i in range(256):
            self.arcs[chr(i)] = 0
        self.arcs[ch_arc_idx] = [p_arc]

    def add(self, ch_arc_idx, p_arc):
        if self.arcs.get(ch_arc_idx) == 0:
            self.arcs[ch_arc_idx] = [p_arc]
        else:
            self.arcs[ch_arc_idx].append(p_arc)

    def display(self, s):
        for i in range(len(self.arcs)):
            curr = self.arcs.get(chr(i))
            if curr != 0:
                for o in range(len(curr)):
                    print(s[curr[o].i_beg:curr[o].i_end + 1])

class Arc:
    """description of class"""
    def __init__(self, i_beg, i_end, p_dest_vert, i_dest_vert):
        self.i_beg = i_beg  # индексы символов метки
        self.i_end = i_end  # в исходной строке
        self.p_dest_vert = p_dest_vert  # вершина, куда входит дуга
        self.i_dest_vert = i_dest_vert  # индекс листа, куда входит дуга



def Find_SuffixTree_Arc(s, substr, m, p_tree):
    p_arc = None # Дуга, на которой остановится поиск
    idx_substr =0 #Индексы несовпавших символов
    idx_arc = 0 #Индексы несовпавших символов
    p_curr_node = p_tree
    b_stopped = 0
    while not b_stopped and p_curr_node:
        p_next_arc = p_curr_node.arcs.get(ord(substr[idx_substr]))
        if p_next_arc:
            # Есть совпадение с начальным символом метки дуги
            p_arc = p_next_arc
            idx_arc = p_arc.i_beg
            while idx_substr < m and idx_arc < p_arc.i_end + 1 and substr[idx_substr] == s[idx_arc]:
                idx_substr += 1
                idx_arc += 1
            if idx_arc <= p_arc.i_end:
                b_stopped = 1 #Не прошли метку
            else:
                #Переход к следующей вершине

                p_curr_node = p_arc.p_dest_vert
        else:
            #Нет продолжения пути
            b_stopped = 1
    if idx_substr == m:
        #Чтобы idxArc было за границей совпадения
        idx_arc += 1
    return p_arc, idx_arc, idx_substr


def St_Build_Naive(s):
    n = len(s)
    p_uv_arc = Arc(0, n - 1, None, 0)
    #Корень дерева и его начальная дуга
    p_tree = Node(s[0], p_uv_arc)
    p_w_node = None
    for i in range(1, n):
        # "Поиск" очередного суффикса на дереве
        p_uv_arc, idxarc, idxsubstr = Find_SuffixTree_Arc(s, s[i:], n - i, p_tree)
        #Поиск остановился в корне
        if not p_uv_arc:
            #Вершина-источник дуги для нового суффикса
            p_w_node = p_tree
        elif idxarc <= p_uv_arc.i_end:
            #Поиск остановился внутри дуги (U, V), требуется ее разделение
            p_w_node = p_tree #Новая разделяющая вершина
            p_w_node.add(s[i], p_uv_arc)
            p_wv_arc = Arc(idxarc, p_uv_arc.i_end, p_uv_arc.p_dest_vert, p_uv_arc.i_dest_vert)#Дуга из W в V
            p_uv_arc.p_dest_vert = p_w_node # Дуга из U в W
            p_uv_arc.i_dest_vert = -1
        else:
            #Поиск остановился в конце дуги (U, V)
            p_w_node = p_uv_arc.p_dest_vert
        p_arc_new = Arc(i + idxsubstr, n - 1, None, i)
        try:
            # Добавить новую дугу из вершины W в лист
            p_w_node.add(s[i + idxsubstr], p_arc_new)
        except IndexError:
            pass
    return p_w_node


def st_leaves_traversal(p_start_arc, n_alpha):
    #pStartArc – стартовая дуга обхода; nAlpha – длина алфавита
    if p_start_arc.i_dest_vert >= 0: #Если дуга направлена к листу
        print("Найдена позиция", p_start_arc.i_dest_vert)
    else:
        #Дуга направлена к внутренней вершине дерева
        p_start_node = p_start_arc.p_dest_vert
        for k in range(n_alpha):
            #Перебор дуг дочерней вершины
            p_arc = p_start_node.arcs[k]
            if p_arc:
                st_leaves_traversal(p_arc, n_alpha)

def open_file():
    while 1:
        try:
            file = input("Choose File: ")
            if not os.path.exists(file):
                raise FileNotFoundError(file)
            break
        except FileNotFoundError:
            print("File does not exist")
    with open(file, 'r') as input_string:
        in_line = ''
        for line in input_string:
            for letter in line:
                if letter is '\n':
                    continue
                in_line += letter
    return in_line

if __name__ == '__main__':
    input_string = open_file()
    print("Initial String", input_string)
    tree = St_Build_Naive(input_string)
    print('Suffix Tree')
    tree.display(input_string)
    for i in range(len(tree.arcs)):
        curr = tree.arcs.get(chr(i))
        if curr != 0:
            for j in range(len(curr)):
                st_leaves_traversal(curr[j], 256)
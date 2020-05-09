class Arc:
    """description of class"""
    def __init__(self, i_beg, i_end, p_dest_vert, i_dest_vert):
        self.i_beg = i_beg  # индексы символов метки
        self.i_end = i_end  # в исходной строке
        self.p_dest_vert = p_dest_vert  # вершина, куда входит дуга
        self.i_dest_vert = i_dest_vert  # индекс листа, куда входит дуга



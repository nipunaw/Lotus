def clear_layout(layout, hide:list=None, keep:list=None):
    if hide is None:
        hide = []
    if keep is None:
        keep = []
    if layout is not None:
        while layout.count():
            pos = 0
            child = layout.takeAt(pos)
            if child.widget() is not None:
                if child.widget() in hide:
                    child.widget().hide()
                elif child.widget() in keep:
                    pos += 1
                else:
                    child.widget().deleteLater()
            elif child.layout() is not None:
                if child.layout() in hide:
                    child.layout().hide()
                clear_layout(child.layout())
    layout.update()


def deleteItemsOfLayout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                deleteItemsOfLayout(item.layout())

def clear_grid(grid_layout, start_row, start_col):
    for row in range(start_row, grid_layout.rowCount()):
        for col in range(start_col, grid_layout.columnCount()):
            item = grid_layout.itemAtPosition(row, col)
            if item.widget() is not None:
                item.widget().deleteLater()
            elif item.layout() is not None:
                deleteItemsOfLayout(item.layout())

def camel_case(string):
    formatted = ""
    split = string.split()
    for j, x in enumerate(split):
        formatted += x.capitalize() + (" " if j != len(split)-1 else "")
    return formatted
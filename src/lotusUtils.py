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
                    print(child.widget())
                    child.widget().deleteLater()
            elif child.layout() is not None:
                print(child.layout())
                if child.layout() in hide:
                    child.layout().hide()
                clear_layout(child.layout())
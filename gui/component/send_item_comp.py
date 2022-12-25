from PyQt6.QtWidgets import QTableWidgetItem


class SendItemBuilder:
    def __init__(self, columns: list[str]):
        self.columns_ = columns

    def build(self) -> list[QTableWidgetItem]:
        items_: list[QTableWidgetItem] = []

        for col_ in self.columns_:
            items_.append(QTableWidgetItem(col_))

        return items_

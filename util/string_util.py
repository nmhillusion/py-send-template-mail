class StringUtil:
    @classmethod
    def is_blank(cls, inp_: str | None):
        return inp_ is None or 0 == len(str(inp_).strip())

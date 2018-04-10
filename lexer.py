from domain.models.quick_statement import QuickStatement


a = QuickStatement("a", "a", "a", [1], [2], [3], [1], [2], [3])
b = QuickStatement("ab", "ab", "ab", [11], [12], [13], [11], [12], [13])
c = []
c.append(a)
c.append(b)

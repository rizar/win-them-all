"""Validator class to make validators from predicates"""
class Validator:
    """Constructor taking predicate"""
    def __init__(self, predicate):
        self.predicate = predicate
    """Validates x by predicate"""
    def __call__(self, x):
        if self.predicate(x):
            return x
        else:
            raise db.BadValueError(x)

import pandas as pd

class DFClassGenerator:

    CLASS_HEADER = 'class {class_name}(pd.DataFrame):'
    COLUMNS = '    {var} = "{label}"'   # we cheat an encode 4 spaces here,for demo

    CONSTRUCTOR =  ("    @property\n"
                    "    def _constructor(self):\n"
                    "        return {class_name}")

    @classmethod
    def generate_class(cls, df, class_name):

        cols = [cls.COLUMNS.format(var=c.upper(), label=c)
                for c in df.columns] # works for single hierarchical column index

        lines = [cls.CLASS_HEADER.format(class_name=class_name)]
        constructor = cls.CONSTRUCTOR.format(class_name=class_name)
        source_code = '\n'.join(lines + cols) + '\n\n' + constructor
        print(source_code)
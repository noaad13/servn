import re

IF = "$#if"
IEQ = "$#ieq"
IFN = "$#ifn"
IEQN = "$#ieqn"
ENDIF = "$#endif"
ENDIEQ = "$#endieq"
ENDIFN = "$#endifn"
ENDIEQN = "$#endieqn"

class TemplateEngine:

    def __init__(self, template_str="", context=None):
        self.tree = {}
        if context is None:
            context = {}
        self.template = template_str
        self.context = context
        self.makeTree()
        self.varsSyntaxed = {}
        for key, value in self.tree.items():
            self.varsSyntaxed["${" + key + "}"] = value

    def getThen(self, tokens, i, end):
        then = ""
        found = False
        for i2 in range(i, len(tokens)):
            tok = tokens[i2]
            if tok == end:
                i = i2 + 1
                found = True
                break
            then += tok
        if not found:
            raise Exception("Invalid syntax")
        return then, i

    def makeTree(self, current=None):
        if current:
            currentObj = self.context
            for cur in current:
                currentObj = currentObj[cur] if isinstance(currentObj, dict) else getattr(currentObj, cur, None)
        else:
            currentObj = self.context
            current = []
        if isinstance(currentObj, dict):
            for key in currentObj:
                self.makeTree(current=current + [key])
        elif hasattr(currentObj, "__dict__"):
            for attr in dir(currentObj):
                if attr.startswith("_"):
                    continue
                try:
                    value = getattr(currentObj, attr)
                    if callable(value):
                        continue
                    self.makeTree(current=current + [attr])
                except Exception:
                    pass
        else:
            path = ".".join(current)
            self.tree[path] = currentObj

    def format(self, templatePart: str):
        for key, value in self.varsSyntaxed.items():
            templatePart = templatePart.replace(key, str(value))
        return templatePart

    def process(self):
        result = ""
        tokens = re.split(r"(\s+)", self.template)
        i = 0
        while True:
            token = tokens[i]
            if token == IF:
                condition = self.varsSyntaxed[tokens[i+2]]
                then, i = self.getThen(tokens, i + 4, ENDIF)
                if condition:
                    result += self.format(then)
            elif token == IEQ:
                value1 = self.format(tokens[i + 2])
                value2 = self.format(tokens[i + 4])
                then, i = self.getThen(tokens, i + 6, ENDIEQ)
                if value1 == value2:
                    result += self.format(then)
            elif token == IFN:
                condition = self.varsSyntaxed[tokens[i + 2]]
                then, i = self.getThen(tokens, i + 4, ENDIFN)
                if not condition:
                    result += self.format(then)
            elif token == IEQN:
                value1 = self.format(tokens[i + 2])
                value2 = self.format(tokens[i + 4])
                then, i = self.getThen(tokens, i + 6, ENDIEQN)
                if value1 != value2:
                    result += self.format(then)
            else:
                result += self.format(token)
                i += 1
            if i >= len(tokens):
                break
        return result

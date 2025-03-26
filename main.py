from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser

class ArithmeticVisitor:
    def __init__(self):
        self.variables = {} # Variáveis definidas pelo usuário

    def visit(self, ctx):
        # Escolhe de acordo com o tipo do nó
        if isinstance(ctx, ArithmeticParser.StatementContext):
            return self.visitStatement(ctx)
        elif isinstance(ctx, ArithmeticParser.AssignmentContext):
            return self.visitAssignment(ctx)
        elif isinstance(ctx, ArithmeticParser.ExprContext):
            return self.visitExpr(ctx)
        elif isinstance(ctx, ArithmeticParser.TermContext):
            return self.visitTerm(ctx)
        elif isinstance(ctx, ArithmeticParser.FactorContext):
            return self.visitFactor(ctx)

    def visitStatement(self, ctx):
        # Entende se é expressão ou assignment
        if ctx.assignment():
            self.visit(ctx.assignment())
            return None
        else:
            return self.visit(ctx.expr())

    def visitAssignment(self, ctx):
        var_name = ctx.VAR().getText()
        value = self.visit(ctx.expr())
        self.variables[var_name] = value

    def visitExpr(self, ctx):
        result = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            op = ctx.getChild(i * 2 - 1).getText()
            # Soma e subtração
            if op == '+':
                result += self.visit(ctx.term(i))
            else:
                result -= self.visit(ctx.term(i))
        return result

    def visitTerm(self, ctx):
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(i * 2 - 1).getText()
            # Multiplicação e divisão
            if op == '*':
                result *= self.visit(ctx.factor(i))
            else:
                divisor = self.visit(ctx.factor(i))
                if divisor == 0:
                    raise Exception("Erro: divisão por zero.")
                result /= divisor
        return result

    def visitFactor(self, ctx):
        # Parenteses
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            var_name = ctx.VAR().getText()
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                raise Exception(f"Variável '{var_name}' não definida.")
        else:
            return self.visit(ctx.expr())

def main():
    print("Digite uma expressão aritmética: ")
    visitor = ArithmeticVisitor()
    while True:
        try:
            line = input(">>> ")
            if not line.strip():
                continue

            # Processamento com ANTLR
            lexer = ArithmeticLexer(InputStream(line))
            stream = CommonTokenStream(lexer)
            parser = ArithmeticParser(stream)
            tree = parser.statement()

            result = visitor.visit(tree)

            if result is not None:
                print("Resultado:", result)

        except EOFError:
            break
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()

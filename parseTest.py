import re
from collections import namedtuple

TOKENIZER = re.compile(r"\w+==\w+|&&|\|\||[()]").findall

Node = namedtuple("Node", ["parent", "children"])


def syntax_tree(text, tokenizer, brackets):
    root = cur_node = Node(None, [])
    stack = []
    for token in tokenizer(text):
        if token == brackets["("]:
            stack.append(token)
            new_node = Node(cur_node, [])
            cur_node.children.append(new_node)
            cur_node = new_node
        elif token == brackets[")"]:
            if stack and stack.pop() == brackets[")"]:
                cur_node = cur_node.parent
            else:
                raise Exception("Parse error: unmatched parentheses")
        else:
            cur_node.children.append(token)

        if stack:
            raise Exception("Parse error: unmatched parentheses")

    return root


def listify(root):
    if isinstance(root, Node):
        return [listify(item) for item in root.children]
    else:
        return root


def order_query(query):
    precedence = {'!': 3, '&': 2, '|': 1, '(': 0, ')': 0}

    output = []
    operator_stack = []

    # while there are tokens to be read
    for token in query.split(' '):

        # if left bracket
        if token == '(':
            operator_stack.append(token)

        # if right bracket, pop all operators from operator stack onto output until we hit left bracket
        elif token == ')':
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()

        # if operator, pop operators from operator stack to queue if they are of higher precedence
        elif token in precedence:
            # if operator stack is not empty
            if operator_stack:
                current_operator = operator_stack[-1]
                while operator_stack and precedence[current_operator] > precedence[token]:
                    output.append(operator_stack.pop())
                    if operator_stack:
                        current_operator = operator_stack[-1]

            operator_stack.append(token)  # add token to stack

        # else if operands, add to output list
        else:
            output.append(token.lower())

    # while there are still operators on the stack, pop them into the queue
    while operator_stack:
        output.append(operator_stack.pop())
    return output


OPERATORS = ['&', '|', '!']
UNARY = ['!']


def get_documents(documents, operands, op):
    if op in UNARY:
        # return documents which staisfy !operands[0]
        pass
    else:  # binary
        pass


def compile_expression(query):
    operands = []
    op = None
    documents = []
    for elem in query:
        if elem not in OPERATORS:
            operands.append(elem)
        else:  # must be operator (unary or binary)
            op = elem
            documents = get_documents(documents, operands, op)
            operands = []
            op = None
    return documents


def compile_term():
    pass


if __name__ == "__main__":
    expr = "((Cat | dog) & mouse) & !love"
    qq = order_query(expr)
    pass

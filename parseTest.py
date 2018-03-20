import db_model

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
    doc_list = []
    if len(documents) == 0:
        if op in UNARY:
            # return documents which staisfy !operands[0]
            pass
        else:  # binary
            if op == "&":
                doc_list = db_model.get_docs_from_2_temp_with_AND(operands[0], operands[1])
            else:
                doc_list = db_model.get_docs_from_2_temp_with_OR(operands[0], operands[1])
    else:
        temp_list = db_model.get_docs_from_single_temp(operands[0])
        if op in UNARY:
            # return documents which staisfy !operands[0]
            pass
        else:  # binary
            if op == "&":
                for x in documents:
                    for y in temp_list:
                        if x[2]==y[2]:
                            doc_list += x
            else:
                doc_list = temp_list + documents
    return doc_list


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
    #zzz = db_model.get_docs_from_single_temp('high')
    #zzz = db_model.get_docs_from_2_temp_with_AND('gingham', 'just')
    expr = "( ( Cat | dog ) & mouse ) & ! love"
    qq = order_query(expr)
    compile_expression(qq)
    pass

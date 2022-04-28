import os
import pickle
from globals import *

symbolStack = []  # 符号栈
syntaxTreeStack = []  # 语法树栈
opStack = []  # 操作符栈
numStack = []  # 操作数栈

getExpResult = 1
expflag = 0
getExpResult2 = 0


def CreatLL1Table():
    global table
    table = {
        LexType.Program: {LexType.PROGRAM: 1},
        LexType.ProgramHead: {LexType.PROGRAM: 2},
        LexType.ProgramName: {LexType.ID: 3},
        LexType.DeclarePart: {LexType.TYPE: 4, LexType.VAR: 4, LexType.PROCEDURE: 4, LexType.BEGIN: 4},
        LexType.TypeDec: {LexType.TYPE: 6, LexType.VAR: 5, LexType.PROCEDURE: 5, LexType.BEGIN: 5},
        LexType.TypeDeclaration: {LexType.TYPE: 7},
        LexType.TypeDecList: {LexType.ID: 8},
        LexType.TypeDecMore: {LexType.VAR: 9, LexType.PROCEDURE: 9, LexType.BEGIN: 9, LexType.ID: 10},
        LexType.TypeId: {LexType.ID: 11},
        LexType.TypeName: {LexType.INTEGER: 12, LexType.CHAR: 12, LexType.ARRAY: 13, LexType.RECORD: 13,
                           LexType.ID: 14},
        LexType.BaseType: {LexType.INTEGER: 15, LexType.CHAR: 16},
        LexType.StructureType: {LexType.ARRAY: 17, LexType.RECORD: 18},
        LexType.ArrayType: {LexType.ARRAY: 19},
        LexType.Low: {LexType.INTC_VAL: 20},
        LexType.Top: {LexType.INTC_VAL: 21},
        LexType.RecType: {LexType.RECORD: 22},
        LexType.FieldDecList: {LexType.INTEGER: 23, LexType.CHAR: 23, LexType.ARRAY: 24},
        LexType.FieldDecMore: {LexType.INTEGER: 26, LexType.CHAR: 26, LexType.ARRAY: 26, LexType.END: 25},
        LexType.IdList: {LexType.ID: 27},
        LexType.IdMore: {LexType.SEMI: 28, LexType.COMMA: 29},
        LexType.VarDec: {LexType.VAR: 31, LexType.PROCEDURE: 30, LexType.BEGIN: 30},
        LexType.VarDeclaration: {LexType.VAR: 32},
        LexType.VarDecList: {LexType.INTEGER: 33, LexType.CHAR: 33, LexType.ARRAY: 33, LexType.RECORD: 33,
                             LexType.ID: 33},
        LexType.VarDecMore: {LexType.INTEGER: 35, LexType.CHAR: 35, LexType.ARRAY: 35, LexType.RECORD: 35,
                             LexType.PROCEDURE: 34, LexType.BEGIN: 34, LexType.ID: 35},
        LexType.VarIdList: {LexType.ID: 36},
        LexType.VarIdMore: {LexType.SEMI: 37, LexType.COMMA: 38},
        LexType.ProcDec: {LexType.PROCEDURE: 40, LexType.BEGIN: 39},
        LexType.ProcDeclaration: {LexType.PROCEDURE: 41},
        LexType.ProcDecMore: {LexType.PROCEDURE: 41, LexType.BEGIN: 42},
        LexType.ProcName: {LexType.ID: 44},
        LexType.ParamList: {LexType.INTEGER: 46, LexType.CHAR: 46, LexType.ARRAY: 46, LexType.RECORD: 46,
                            LexType.VAR: 46, LexType.ID: 46, LexType.RMIDPAREN: 45},
        LexType.ParamDecList: {LexType.INTEGER: 47, LexType.CHAR: 47, LexType.ARRAY: 47, LexType.RECORD: 47,
                               LexType.VAR: 47, LexType.ID: 47},
        LexType.ParamMore: {LexType.SEMI: 49, LexType.RPAREN: 48},
        LexType.Param: {LexType.INTEGER: 50, LexType.CHAR: 50, LexType.ARRAY: 50, LexType.RECORD: 50, LexType.END: 51,
                        LexType.ID: 50, LexType.VAR: 51},
        LexType.FormList: {LexType.ID: 52},
        LexType.FidMore: {LexType.SEMI: 53, LexType.COMMA: 54, LexType.RPAREN: 53},
        LexType.ProcDecPart: {LexType.TYPE: 55, LexType.VAR: 55, LexType.PROCEDURE: 55, LexType.BEGIN: 55},
        LexType.ProcBody: {LexType.BEGIN: 56},
        LexType.ProgramBody: {LexType.BEGIN: 57},
        LexType.StmList: {LexType.IF: 58, LexType.WHILE: 58, LexType.READ: 58, LexType.WRITE: 58, LexType.RETURN: 58,
                          LexType.ID: 58},
        LexType.StmMore: {LexType.END: 59, LexType.ELSE: 59, LexType.FI: 59, LexType.ENDWH: 59, LexType.SEMI: 60},
        LexType.Stm: {LexType.IF: 61, LexType.WHILE: 62, LexType.READ: 63, LexType.WRITE: 64, LexType.RETURN: 65,
                      LexType.ID: 66},
        LexType.AssCall: {LexType.ASSIGN: 67, LexType.DOT: 67, LexType.LMIDPAREN: 67, LexType.LPAREN: 68},
        LexType.AssignmentRest: {LexType.DOT: 69, LexType.LMIDPAREN: 69, LexType.ASSIGN: 69},
        LexType.ConditionalStm: {LexType.IF: 70},
        LexType.LoopStm: {LexType.WHILE: 71},
        LexType.InputStm: {LexType.READ: 72},
        LexType.Invar: {LexType.ID: 73},
        LexType.OutputStm: {LexType.WRITE: 74},
        LexType.ReturnStm: {LexType.RETURN: 75},
        LexType.CallStmRest: {LexType.LPAREN: 76},
        LexType.ActParamList: {LexType.INTC_VAL: 78, LexType.ID: 78, LexType.LPAREN: 78, LexType.RPAREN: 77},
        LexType.ActParamMore: {LexType.COMMA: 80, LexType.RPAREN: 79},
        LexType.RelExp: {LexType.INTC_VAL: 81, LexType.ID: 81, LexType.LMIDPAREN: 81},
        LexType.OtherRelE: {LexType.LT: 82, LexType.EQ: 82},
        LexType.Exp: {LexType.INTC_VAL: 83, LexType.ID: 83, LexType.LPAREN: 83},
        LexType.OtherFactor: {LexType.END: 87, LexType.THEN: 87, LexType.ELSE: 87, LexType.FI: 87, LexType.DO: 87,
                              LexType.ENDWH: 87,
                              LexType.SEMI: 87, LexType.COMMA: 87, LexType.RPAREN: 87, LexType.RMIDPAREN: 87,
                              LexType.LT: 87, LexType.EQ: 87,
                              LexType.PLUS: 87, LexType.MINUS: 87, LexType.TIMES: 88, LexType.DIVIDE: 88},
        LexType.Term: {LexType.INTC_VAL: 86, LexType.END: 87, LexType.THEN: 87, LexType.ELSE: 87, LexType.FI: 87,
                       LexType.DO: 87, LexType.ENDWH: 87,
                       LexType.ID: 86, LexType.SEMI: 87, LexType.COMMA: 87, LexType.LPAREN: 86, LexType.RPAREN: 87,
                       LexType.RMIDPAREN: 87,
                       LexType.LT: 87, LexType.EQ: 87, LexType.PLUS: 87, LexType.MINUS: 87, LexType.TIMES: 88,
                       LexType.DIVIDE: 88
                       },
        LexType.Factor: {LexType.INTC_VAL: 90, LexType.ID: 91, LexType.LPAREN: 89},
        LexType.OtherTerm: {LexType.END: 84, LexType.THEN: 84, LexType.ELSE: 84, LexType.FI: 84, LexType.DO: 84,
                            LexType.ENDWH: 84,
                            LexType.SEMI: 84, LexType.COMMA: 84, LexType.RPAREN: 84, LexType.RMIDPAREN: 84,
                            LexType.LT: 84,
                            LexType.EQ: 84, LexType.PLUS: 85, LexType.MINUS: 85},
        LexType.VariMore: {LexType.END: 93, LexType.THEN: 93, LexType.ELSE: 93, LexType.FI: 93, LexType.DO: 93,
                           LexType.ENDWH: 93,
                           LexType.DOT: 95, LexType.SEMI: 93, LexType.COMMA: 93, LexType.RPAREN: 93,
                           LexType.LMIDPAREN: 94,
                           LexType.RMIDPAREN: 93, LexType.LT: 93, LexType.EQ: 93, LexType.PLUS: 93, LexType.MINUS: 93,
                           LexType.TIMES: 93, LexType.DIVIDE: 93, LexType.ASSIGN: 93},
        LexType.FieldVarMore: {LexType.END: 97, LexType.THEN: 97, LexType.ELSE: 97, LexType.FI: 97, LexType.DO: 97,
                               LexType.ENDWH: 97,
                               LexType.SEMI: 97, LexType.COMMA: 97, LexType.RPAREN: 97, LexType.LMIDPAREN: 98,
                               LexType.RMIDPAREN: 97,
                               LexType.LT: 97, LexType.EQ: 97, LexType.PLUS: 97, LexType.MINUS: 97, LexType.TIMES: 97,
                               LexType.DIVIDE: 97,
                               LexType.ASSIGN: 97},
        LexType.Variable: {LexType.ID: 92},
        LexType.FieldVar: {LexType.ID: 96},

        LexType.CmpOp: {LexType.LT: 99, LexType.EQ: 100},
        LexType.AddOp: {LexType.PLUS: 101, LexType.MINUS: 102},
        LexType.MultOp: {LexType.TIMES: 103, LexType.DIVIDE: 104},
    }


def Priosity(op):
    if op == LexType.END:
        pri = -1
    elif op == LexType.LPAREN:  # 左括号
        pri = 0
    elif op == LexType.LT or op == LexType.EQ:
        pri = 1
    elif op == LexType.PLUS or op == LexType.MINUS:
        pri = 2
    elif op == LexType.TIMES or op == LexType.DIVIDE:
        pri = 3
    else:
        print("没有这个操作符")
        pri = -1
    return pri


def process(id, token=None, root=None):
    global temp, currentTreeNode, saveP, getExpResult2, getExpResult, expflag  # 0 false 1 true
    # 赋初值
    if id == 1:
        symbolStack.append(LexType.DOT)
        symbolStack.append(LexType.ProgramBody)
        symbolStack.append(LexType.DeclarePart)
        symbolStack.append(LexType.ProgramHead)
    elif id == 2:
        symbolStack.append(LexType.ProgramName)
        symbolStack.append(LexType.PROGRAM)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.PheadK
        # syntaxTreeStack[len(syntaxTreeStack) - 1].line = token.line
        currentTreeNode = syntaxTreeStack.pop()
    elif id == 3:
        symbolStack.append(LexType.ID)
        currentTreeNode.name[0] = token.sem
        currentTreeNode.idnum = currentTreeNode.idnum + 1
    elif id == 4:
        symbolStack.append(LexType.ProcDec)
        symbolStack.append(LexType.VarDec)
        symbolStack.append(LexType.TypeDec)
    elif id == 5:
        return
    elif id == 6:
        symbolStack.append(LexType.TypeDeclaration)
    elif id == 7:
        symbolStack.append(LexType.TypeDecList)
        symbolStack.append(LexType.TYPE)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.TypeK
        # syntaxTreeStack[len(syntaxTreeStack) - 1].line = token.line
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setchild0()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
        syntaxTreeStack.append(currentTreeNode.child[0])
    elif id == 8:
        symbolStack.append(LexType.TypeDecMore)
        symbolStack.append(LexType.SEMI)
        symbolStack.append(LexType.TypeName)
        symbolStack.append(LexType.EQ)
        symbolStack.append(LexType.TypeId)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.DecK
        # syntaxTreeStack[len(syntaxTreeStack) - 1].line = token.line
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 9:
        syntaxTreeStack.pop()
    elif id == 10:
        symbolStack.append(LexType.TypeDecList)
    elif id == 11:
        symbolStack.append(LexType.ID)
        currentTreeNode.name[0] = token.sem
        currentTreeNode.idnum = currentTreeNode.idnum + 1
    elif id == 12:
        symbolStack.append(LexType.BaseType)
        temp = currentTreeNode.kind
    elif id == 13:
        symbolStack.append(LexType.StructureType)
    elif id == 14:
        symbolStack.append(LexType.ID)
        currentTreeNode.kind["dec"] = DecKind.IdK
        currentTreeNode.type_name = token.sem  # 落下了这条语句
        currentTreeNode.idnum = currentTreeNode.idnum + 1
    elif id == 15:
        symbolStack.append(LexType.INTEGER)
        temp["dec"] = DecKind.IntegerK
        temp["childtype"] = DecKind.IntegerK
    elif id == 16:
        symbolStack.append(LexType.CHAR)
        temp["dec"] = DecKind.CharK
    elif id == 17:
        symbolStack.append(LexType.ArrayType)
    elif id == 18:
        symbolStack.append(LexType.RecType)
    elif id == 19:  # o (half of ok)
        symbolStack.append(LexType.BaseType)
        symbolStack.append(LexType.OF)
        symbolStack.append(LexType.RMIDPAREN)
        symbolStack.append(LexType.Top)
        symbolStack.append(LexType.UNDERRANGE)
        symbolStack.append(LexType.Low)
        symbolStack.append(LexType.LMIDPAREN)
        symbolStack.append(LexType.ARRAY)
        currentTreeNode.kind["dec"] = DecKind.ArrayK
        # temp = currentTreeNode.attr["ArrayAttr"]["childtype"]
        temp = currentTreeNode.attr["ArrayAttr"]
    elif id == 20:
        symbolStack.append(LexType.INTC_VAL)
        currentTreeNode.attr["ArrayAttr"]["low"] = int(token.sem)
    elif id == 21:
        symbolStack.append(LexType.INTC_VAL)
        currentTreeNode.attr["ArrayAttr"]["up"] = int(token.sem)
    elif id == 22:
        symbolStack.append(LexType.END)
        symbolStack.append(LexType.FieldDecList)
        symbolStack.append(LexType.RECORD)
        currentTreeNode.kind["dec"] = DecKind.RecordK
        currentTreeNode.setchild0()
        saveP = currentTreeNode
        syntaxTreeStack.append(currentTreeNode.child[0])
    elif id == 23:
        symbolStack.append(LexType.FieldDecMore)
        symbolStack.append(LexType.SEMI)
        symbolStack.append(LexType.IdList)
        symbolStack.append(LexType.BaseType)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.DecK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        temp = currentTreeNode.kind  # dec
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 24:
        symbolStack.append(LexType.FieldDecMore)
        symbolStack.append(LexType.SEMI)
        symbolStack.append(LexType.IdList)
        symbolStack.append(LexType.ArrayType)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.DecK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 25:
        syntaxTreeStack.pop()
        currentTreeNode = saveP
    elif id == 26:
        symbolStack.append(LexType.FieldDecList)
    elif id == 27:
        symbolStack.append(LexType.IdMore)
        symbolStack.append(LexType.ID)
        currentTreeNode.name[currentTreeNode.idnum] = token.sem
        currentTreeNode.idnum = currentTreeNode.idnum + 1
    elif id == 28:
        return
    elif id == 29:
        symbolStack.append(LexType.IdList)
        symbolStack.append(LexType.COMMA)
    elif id == 30:
        return
    elif id == 31:
        symbolStack.append(LexType.VarDeclaration)
    elif id == 32:
        symbolStack.append(LexType.VarDecList)
        symbolStack.append(LexType.VAR)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.VarK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        currentTreeNode.setchild0()
        syntaxTreeStack.append(currentTreeNode.brother)
        syntaxTreeStack.append(currentTreeNode.child[0])
    elif id == 33:
        symbolStack.append(LexType.VarDecMore)
        symbolStack.append(LexType.SEMI)
        symbolStack.append(LexType.VarIdList)
        symbolStack.append(LexType.TypeName)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.DecK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 34:
        syntaxTreeStack.pop()
    elif id == 35:
        symbolStack.append(LexType.VarDecList)
    elif id == 36:
        symbolStack.append(LexType.VarIdMore)
        symbolStack.append(LexType.ID)
        currentTreeNode.name[currentTreeNode.idnum] = token.sem
        currentTreeNode.idnum = currentTreeNode.idnum + 1
    elif id == 37:
        return
    elif id == 38:
        symbolStack.append(LexType.VarIdList)
        symbolStack.append(LexType.COMMA)
    elif id == 39:
        return
    elif id == 40:
        symbolStack.append(LexType.ProcDeclaration)
    elif id == 41:
        symbolStack.append(LexType.ProcDecMore)
        symbolStack.append(LexType.ProcBody)
        symbolStack.append(LexType.ProcDecPart)
        symbolStack.append(LexType.SEMI)
        symbolStack.append(LexType.RPAREN)
        symbolStack.append(LexType.ParamList)
        symbolStack.append(LexType.LPAREN)
        symbolStack.append(LexType.ProcName)
        symbolStack.append(LexType.PROCEDURE)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.ProcDecK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        currentTreeNode.setchild0()
        currentTreeNode.setchild1()
        currentTreeNode.setchild2()
        syntaxTreeStack.append(currentTreeNode.brother)
        syntaxTreeStack.append(currentTreeNode.child[2])
        syntaxTreeStack.append(currentTreeNode.child[1])
        syntaxTreeStack.append(currentTreeNode.child[0])
    elif id == 42:
        return
    elif id == 43:
        symbolStack.append(LexType.ProcDeclaration)
    elif id == 44:
        symbolStack.append(LexType.ID)
        currentTreeNode.name[0] = token.sem  # 是name[0]
        currentTreeNode.idnum = currentTreeNode.idnum + 1
    elif id == 45:
        syntaxTreeStack.pop()
    elif id == 46:
        symbolStack.append(LexType.ParamDecList)
    elif id == 47:
        symbolStack.append(LexType.ParamMore)
        symbolStack.append(LexType.Param)
    elif id == 48:
        syntaxTreeStack.pop()
    elif id == 49:
        symbolStack.append(LexType.ParamDecList)
        symbolStack.append(LexType.SEMI)
    elif id == 50:
        symbolStack.append(LexType.FormList)
        symbolStack.append(LexType.TypeName)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.DecK
        syntaxTreeStack[len(syntaxTreeStack) - 1].attr["ProcAttr"]["paramt"] = ParamType.valparamType
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 51:
        symbolStack.append(LexType.FormList)
        symbolStack.append(LexType.TypeName)
        symbolStack.append(LexType.VAR)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.DecK
        syntaxTreeStack[len(syntaxTreeStack) - 1].attr["ProcAttr"]["paramt"] = ParamType.varparamType
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 52:
        symbolStack.append(LexType.FidMore)
        symbolStack.append(LexType.ID)
        currentTreeNode.name[currentTreeNode.idnum] = token.sem
        currentTreeNode.idnum = currentTreeNode.idnum + 1
    elif id == 53:
        return
    elif id == 54:
        symbolStack.append(LexType.FormList)
        symbolStack.append(LexType.COMMA)
    elif id == 55:
        symbolStack.append(LexType.DeclarePart)
    elif id == 56:
        symbolStack.append(LexType.ProgramBody)
    elif id == 57:
        symbolStack.append(LexType.END)
        symbolStack.append(LexType.StmList)
        symbolStack.append(LexType.BEGIN)
        # 注意，若没有声明部分，则弹出的是程序或过程根节点中指向
        # 声明部分的指针child[1];
        # 若有声明部分，则弹出的是语句序列前
        # 的最后一个声明标识节点的兄弟指针；不管是哪种情况，都正好
        # 需要弹出语法树栈中的一个指针
        syntaxTreeStack.pop()
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.StmLK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setchild0()
        syntaxTreeStack.append(currentTreeNode.child[0])
    elif id == 58:
        symbolStack.append(LexType.StmMore)
        symbolStack.append(LexType.Stm)
    elif id == 59:
        syntaxTreeStack.pop()
    elif id == 60:
        symbolStack.append(LexType.StmList)
        symbolStack.append(LexType.SEMI)
    elif id == 61:
        symbolStack.append(LexType.ConditionalStm)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.StmtK
        syntaxTreeStack[len(syntaxTreeStack) - 1].kind["stmt"] = StmtKind.IfK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 62:
        symbolStack.append(LexType.LoopStm)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.StmtK
        syntaxTreeStack[len(syntaxTreeStack) - 1].kind["stmt"] = StmtKind.WhileK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 63:
        symbolStack.append(LexType.InputStm)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.StmtK
        syntaxTreeStack[len(syntaxTreeStack) - 1].kind["stmt"] = StmtKind.ReadK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 64:
        symbolStack.append(LexType.OutputStm)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.StmtK
        syntaxTreeStack[len(syntaxTreeStack) - 1].kind["stmt"] = StmtKind.WriteK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 65:
        symbolStack.append(LexType.ReturnStm)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.StmtK
        syntaxTreeStack[len(syntaxTreeStack) - 1].kind["stmt"] = StmtKind.ReturnK
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 66:
        symbolStack.append(LexType.AssCall)
        symbolStack.append(LexType.ID)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.StmtK
        syntaxTreeStack[len(syntaxTreeStack) - 1].kind["stmt"] = StmtKind.AssignK
        t = TreeNode(NodeKind.ExpK)
        t.kind["exp"] = ExpKind.VariK
        t.name[0] = token.sem
        t.idnum = t.idnum + 1
        syntaxTreeStack[len(syntaxTreeStack) - 1].child[0] = t
        currentTreeNode = syntaxTreeStack.pop()
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
    elif id == 67:
        symbolStack.append(LexType.AssignmentRest)
        currentTreeNode.kind["stmt"] = StmtKind.AssignK
    elif id == 68:
        symbolStack.append(LexType.CallStmRest)
        # print(currentTreeNode.child[0])  #child[0] is not none
        currentTreeNode.child[0].attr["ExpAttr"]["varkind"] = VarKind.IdV
        currentTreeNode.kind["stmt"] = StmtKind.CallK
    elif id == 69:
        symbolStack.append(LexType.Exp)
        symbolStack.append(LexType.ASSIGN)
        symbolStack.append(LexType.VariMore)
        currentTreeNode.setchild1()
        syntaxTreeStack.append(currentTreeNode.child[1])
        # print(currentTreeNode.child[0])   # child[0] 不为None
        currentTreeNode = currentTreeNode.child[0]  # 当前指针指向赋值左部
        t = TreeNode(NodeKind.ExpK)
        t.kind["exp"] = ExpKind.OpK
        t.attr["ExpAttr"]["op"] = LexType.END  # 操作符栈的栈底存入一个特殊的操作符作为标志
        opStack.append(t)
    elif id == 70:
        symbolStack.append(LexType.FI)
        symbolStack.append(LexType.StmList)
        symbolStack.append(LexType.ELSE)
        symbolStack.append(LexType.StmList)
        symbolStack.append(LexType.THEN)
        symbolStack.append(LexType.RelExp)
        symbolStack.append(LexType.IF)
        currentTreeNode.setchild()
        syntaxTreeStack.append(currentTreeNode.child[2])
        syntaxTreeStack.append(currentTreeNode.child[1])
        syntaxTreeStack.append(currentTreeNode.child[0])
    elif id == 71:
        symbolStack.append(LexType.ENDWH)
        symbolStack.append(LexType.StmList)
        symbolStack.append(LexType.DO)
        symbolStack.append(LexType.RelExp)
        symbolStack.append(LexType.WHILE)
        currentTreeNode.setchild1()
        currentTreeNode.setchild0()
        syntaxTreeStack.append(currentTreeNode.child[1])
        syntaxTreeStack.append(currentTreeNode.child[0])
    elif id == 72:
        symbolStack.append(LexType.RPAREN)
        symbolStack.append(LexType.Invar)
        symbolStack.append(LexType.LPAREN)
        symbolStack.append(LexType.READ)
    elif id == 73:
        symbolStack.append(LexType.ID)
        currentTreeNode.name[0] = token.sem  # 到底给0还是idnum赋值
        currentTreeNode.idnum = currentTreeNode.idnum + 1
    elif id == 74:
        symbolStack.append(LexType.RPAREN)
        symbolStack.append(LexType.Exp)
        symbolStack.append(LexType.LPAREN)
        symbolStack.append(LexType.WRITE)
        currentTreeNode.setchild0()  # 找了好久的bug
        syntaxTreeStack.append(currentTreeNode.child[0])
        t = TreeNode(NodeKind.ExpK)
        t.kind["exp"] = ExpKind.OpK
        t.attr["ExpAttr"]["op"] = LexType.END  # 操作符栈的栈底存入一个特殊的操作符作为标志
        opStack.append(t)
    elif id == 75:
        symbolStack.append(LexType.RETURN)
    elif id == 76:
        symbolStack.append(LexType.RPAREN)
        symbolStack.append(LexType.ActParamList)
        symbolStack.append(LexType.LPAREN)
        currentTreeNode.setchild1()
        syntaxTreeStack.append(currentTreeNode.child[1])
    elif id == 77:
        syntaxTreeStack.pop()
    elif id == 78:
        symbolStack.append(LexType.ActParamMore)
        symbolStack.append(LexType.Exp)
        t = TreeNode(NodeKind.ExpK)
        t.kind["exp"] = ExpKind.OpK
        t.attr["ExpAttr"]["op"] = LexType.END  # 操作符栈的栈底存入一个特殊的操作符作为标志
        opStack.append(t)
    elif id == 79:
        return
    elif id == 80:
        symbolStack.append(LexType.ActParamList)
        symbolStack.append(LexType.COMMA)
        currentTreeNode.setbro()
        syntaxTreeStack.append(currentTreeNode.brother)
        # -------------------------------表达式部分-----------------------------------
    elif id == 81:
        symbolStack.append(LexType.OtherRelE)
        symbolStack.append(LexType.Exp)
        t = TreeNode(NodeKind.ExpK)
        t.kind["exp"] = ExpKind.OpK
        t.attr["ExpAttr"]["op"] = LexType.END  # 操作符栈的栈底存入一个特殊的操作符作为标志
        opStack.append(t)
        getExpResult = 0
    elif id == 82:
        symbolStack.append(LexType.Exp)
        symbolStack.append(LexType.CmpOp)
        currentTreeNode = TreeNode(NodeKind.ExpK)
        currentTreeNode.kind["exp"] = ExpKind.OpK
        currentTreeNode.attr["ExpAttr"]["op"] = token.lex
        sTop = opStack[len(opStack) - 1].attr["ExpAttr"]["op"]
        while Priosity(sTop) >= Priosity(token.lex):
            t = opStack.pop()
            Rnum = numStack.pop()
            Lnum = numStack.pop()
            t.child[1] = Rnum
            t.child[0] = Lnum
            numStack.append(t)
            sTop = opStack[len(opStack) - 1].attr["ExpAttr"]["op"]
        opStack.append(currentTreeNode)
        getExpResult = 1
    elif id == 83:
        symbolStack.append(LexType.OtherTerm)
        symbolStack.append(LexType.Term)
    elif id == 84:
        if token.lex == LexType.RPAREN and expflag != 0:
            while opStack[len(opStack) - 1].attr["ExpAttr"]["op"] != LexType.LPAREN:
                t = opStack.pop()
                Rnum = numStack.pop()
                Lnum = numStack.pop()
                t.child[1] = Rnum
                t.child[0] = Lnum
                numStack.append(t)
            expflag = expflag - 1
        else:
            if getExpResult or getExpResult2:
                while opStack[len(opStack) - 1].attr["ExpAttr"]["op"] != LexType.END:
                    t = opStack.pop()
                    Rnum = numStack.pop()
                    Lnum = numStack.pop()
                    t.child[1] = Rnum
                    t.child[0] = Lnum
                    numStack.append(t)
                opStack.pop()
                # print(syntaxTreeStack)    # 栈存在None  下一句就会报错
                syntaxTreeStack[len(syntaxTreeStack) - 1] = copyTreeNode(syntaxTreeStack[len(syntaxTreeStack) - 1],
                                                                         numStack.pop())
                syntaxTreeStack.pop()
                if getExpResult2 == 1:
                    getExpResult2 = 0
    elif id == 85:
        symbolStack.append(LexType.Exp)
        symbolStack.append(LexType.AddOp)
        currentTreeNode = TreeNode(NodeKind.ExpK)
        currentTreeNode.kind["exp"] = ExpKind.OpK  # QT新声明了
        currentTreeNode.attr["ExpAttr"]["op"] = token.lex
        sTop = opStack[len(opStack) - 1].attr["ExpAttr"]["op"]
        while Priosity(sTop) >= Priosity(token.lex):
            t = opStack.pop()
            Rnum = numStack.pop()
            Lnum = numStack.pop()
            t.child[1] = Rnum
            t.child[0] = Lnum
            numStack.append(t)
            sTop = opStack[len(opStack) - 1].attr["ExpAttr"]["op"]
        opStack.append(currentTreeNode)
    elif id == 86:
        symbolStack.append(LexType.OtherFactor)
        symbolStack.append(LexType.Factor)
    elif id == 87:
        return
    elif id == 88:
        symbolStack.append(LexType.Term)
        symbolStack.append(LexType.MultOp)
        currentTreeNode = TreeNode(NodeKind.ExpK)
        currentTreeNode.kind["exp"] = ExpKind.OpK  # QT新声明了
        currentTreeNode.attr["ExpAttr"]["op"] = token.lex
        sTop = opStack[len(opStack) - 1].attr["ExpAttr"]["op"]
        while Priosity(sTop) >= Priosity(token.lex):
            t = opStack.pop()
            Rnum = numStack.pop()
            Lnum = numStack.pop()
            t.child[1] = Rnum
            t.child[0] = Lnum
            numStack.append(t)
            sTop = opStack[len(opStack) - 1].attr["ExpAttr"]["op"]
        opStack.append(currentTreeNode)
    elif id == 89:
        symbolStack.append(LexType.RPAREN)
        symbolStack.append(LexType.Exp)
        symbolStack.append(LexType.LPAREN)
        t = TreeNode(NodeKind.ExpK)
        t.kind["exp"] = ExpKind.OpK  # QT新声明了
        t.attr["ExpAttr"]["op"] = token.lex
        opStack.append(t)
        expflag = expflag + 1
    elif id == 90:
        symbolStack.append(LexType.INTC_VAL)
        t = TreeNode(NodeKind.ExpK)  # QT新声明了
        t.kind["exp"] = ExpKind.ConstK
        t.attr["ExpAttr"]["val"] = int(token.sem)
        t.attr["ExpAttr"]["varkind"] = VarKind.IdV   # qt没有 自己后加的
        numStack.append(t)
    elif id == 91:
        symbolStack.append(LexType.Variable)
    elif id == 92:
        symbolStack.append(LexType.VariMore)
        symbolStack.append(LexType.ID)
        currentTreeNode = TreeNode(NodeKind.ExpK)
        currentTreeNode.kind["exp"] = ExpKind.VariK
        currentTreeNode.name[0] = token.sem
        currentTreeNode.idnum = currentTreeNode.idnum + 1
        numStack.append(currentTreeNode)
    elif id == 93:
        currentTreeNode.attr["ExpAttr"]["varkind"] = VarKind.IdV
    elif id == 94:
        symbolStack.append(LexType.RMIDPAREN)
        symbolStack.append(LexType.Exp)
        symbolStack.append(LexType.LMIDPAREN)
        currentTreeNode.attr["ExpAttr"]["varkind"] = VarKind.ArrayMembV
        currentTreeNode.setchild0()
        syntaxTreeStack.append(currentTreeNode.child[0])
        t = TreeNode(NodeKind.ExpK)
        t.kind["exp"] = ExpKind.OpK  # QT新声明了
        t.attr["ExpAttr"]["op"] = LexType.END
        opStack.append(t)
        getExpResult2 = 1
    elif id == 95:
        symbolStack.append(LexType.FieldVar)
        symbolStack.append(LexType.DOT)
        currentTreeNode.attr["ExpAttr"]["varkind"] = VarKind.FieldMembV
        currentTreeNode.setchild0()
        syntaxTreeStack.append(currentTreeNode.child[0])
    elif id == 96:
        symbolStack.append(LexType.FieldVarMore)
        symbolStack.append(LexType.ID)
        syntaxTreeStack[len(syntaxTreeStack) - 1].nodekind = NodeKind.ExpK
        syntaxTreeStack[len(syntaxTreeStack) - 1].kind["exp"] = ExpKind.VariK
        syntaxTreeStack[len(syntaxTreeStack) - 1].name[0] = token.sem
        syntaxTreeStack[len(syntaxTreeStack) - 1].idnum = currentTreeNode.idnum + 1
        currentTreeNode = syntaxTreeStack.pop()
    elif id == 97:
        currentTreeNode.attr["ExpAttr"]["varkind"] = VarKind.IdV
    elif id == 98:
        symbolStack.append(LexType.RMIDPAREN)
        symbolStack.append(LexType.Exp)
        symbolStack.append(LexType.LMIDPAREN)
        currentTreeNode.attr["ExpAttr"]["varkind"] = VarKind.ArrayMembV
        currentTreeNode.setchild0()
        syntaxTreeStack.append(currentTreeNode.child[0])
        t = TreeNode(NodeKind.ExpK)
        t.kind["exp"] = ExpKind.OpK  # QT新声明了
        t.attr["ExpAttr"]["op"] = LexType.END
        opStack.append(t)
        getExpResult2 = 1
    elif id == 99:
        symbolStack.append(LexType.LT)
    elif id == 100:
        symbolStack.append(LexType.EQ)
    elif id == 101:
        symbolStack.append(LexType.PLUS)
    elif id == 102:
        symbolStack.append(LexType.MINUS)
    elif id == 103:
        symbolStack.append(LexType.TIMES)
    elif id == 104:
        symbolStack.append(LexType.DIVIDE)


# 获取下一个token
def readNextToken():
    global tokenPos, tokenList
    if tokenPos < len(tokenList):
        t = tokenList[tokenPos]
        tokenPos = tokenPos + 1
    else:
        t = Token()
    return t


def parseLL():
    CreatLL1Table()
    symbolStack.append(LexType.Program)
    root = TreeNode(NodeKind.ProK)
    root.setchild()
    root.setbro()
    syntaxTreeStack.append(root.child[2])
    syntaxTreeStack.append(root.child[1])
    syntaxTreeStack.append(root.child[0])
    token = readNextToken()
    lineno = token.line
    while len(symbolStack) != 0:  # 符号栈非空
        if token == None:
            exit(0)
        if 40 <= symbolStack[len(symbolStack) - 1].value <= 109:
            ss = symbolStack.pop()
            pnum = table[ss][token.lex]
            if 1 <= pnum <= 104:
                process(pnum, token, root)
            else:
                print("I don't understand the:", token.lex, "in this line:", lineno)
        if -2 <= symbolStack[len(symbolStack) - 1].value <= 39:
            if symbolStack[len(symbolStack) - 1] == token.lex:
                symbolStack.pop()
                token = readNextToken()
                lineno = token.line
            else:
                print("unexpected token:", token.lex, "in line:", lineno)
                token = readNextToken()
    # 分析成功  打印语法树
    printTree(root, 0)


# 打印token序列
def showTokenlist(list):
    for token in list:
        print(token.getString())


if __name__ == '__main__':
    global scanToken, tokenList, currentLine, root, tokenPos
    scanToken = "tokenList.data"  # token序列存储的数据
    tokenList = []
    currentLine = 0
    tokenPos = 0
    if not os.path.isdir("record"):
        os.mkdir("record")
    os.chdir("record")
    if not os.path.isfile(scanToken):
        print(scanToken + "don't exist!")
        exit(-1)
    # 读token数据
    fp = open(scanToken, 'rb')
    tokenList = pickle.load(fp)
    fp.close()
    os.chdir("..")
    # showTokenlist(tokenList)  # 打印生成的token序列
    parseLL()  # 调用LL1语法分析程序

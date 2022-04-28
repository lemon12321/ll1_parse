import copy
from enum import Enum, auto


class LexType(Enum):
    # 终极符
    ENDFILE = -2
    ERROR = -1
    PROGRAM = 0
    PROCEDURE = 1
    TYPE = 2
    VAR = 3
    IF = 4
    THEN = 5
    ELSE = 6
    FI = 7
    WHILE = 8
    DO = 9
    ENDWH = 10
    BEGIN = 11
    END = 12
    READ = 13
    WRITE = 14
    ARRAY = 15
    OF = 16
    RECORD = 17
    RETURN = 18
    INTEGER = 19
    CHAR = 20
    ID = 21
    INTC_VAL = 22
    CHARC_VAL = 23
    ASSIGN = 24
    EQ = 25
    LT = 26
    PLUS = 27
    MINUS = 28
    TIMES = 29
    DIVIDE = 30
    LPAREN = 31
    RPAREN = 32
    DOT = 33
    COLON = 34
    SEMI = 35
    COMMA = 36
    LMIDPAREN = 37
    RMIDPAREN = 38
    UNDERRANGE = 39
    # 非终极符
    Program = 40
    ProgramHead = 41
    ProgramName = 42
    DeclarePart = 43
    TypeDec = 44
    TypeDeclaration = 45
    TypeDecList = auto()
    TypeDecMore = auto()
    TypeId = auto()
    TypeName = auto()
    BaseType = auto()
    StructureType = auto()
    ArrayType = auto()
    Low = auto()
    Top = auto()
    RecType = auto()
    FieldDecList = auto()
    FieldDecMore = auto()
    IdList = auto()
    IdMore = auto()
    VarDec = auto()
    VarDeclaration = auto()
    VarDecList = auto()
    VarDecMore = auto()
    VarIdList = auto()
    VarIdMore = auto()
    ProcDec = auto()
    ProcDeclaration = auto()
    ProcDecMore = auto()
    ProcName = auto()
    ParamList = auto()
    ParamDecList = auto()
    ParamMore = auto()
    Param = auto()
    FormList = auto()
    FidMore = auto()
    ProcDecPart = auto()
    ProcBody = auto()
    ProgramBody = auto()
    StmList = auto()
    StmMore = auto()
    Stm = auto()
    AssCall = auto()
    AssignmentRest = auto()
    ConditionalStm = auto()
    StmL = auto()
    LoopStm = auto()
    InputStm = auto()
    Invar = auto()
    OutputStm = auto()
    ReturnStm = auto()
    CallStmRest = auto()
    ActParamList = auto()
    ActParamMore = auto()
    RelExp = auto()
    OtherRelE = auto()
    Exp = auto()
    OtherTerm = auto()
    Term = auto()
    OtherFactor = auto()
    Factor = auto()
    Variable = auto()
    VariMore = auto()
    FieldVar = auto()
    FieldVarMore = auto()
    CmpOp = auto()
    AddOp = auto()
    MultOp = auto()  # 109
    DEFAULT = auto()  # 默认


# 语法树节点结构
class TreeNode:
    def __init__(self, nodekind=None):
        self.brother = None  # 指向兄弟节点的指针
        self.child = [None, None, None]
        self.line = 0  # 行数
        self.nodekind = nodekind  # 节点类型s
        self.kind = {"dec": None, "stmt": None, "exp": None}  # 节点具体类型(声明，语句，表达式)
        self.idnum = 0  # 标识符个数
        self.name = [""] * 10  # 记录标识符
        self.table = [None] * 10  # 记录各标识符在符号表的入口
        self.type_name = ""  # 记录类型名
        self.attr = {
            "ArrayAttr": {"low": 0, "up": 0, "childtype": None},  # 数组类型的信息
            "ProcAttr": {"paramt": None},  # 过程的参数类型（值参、变参）
            "ExpAttr": {"op": None, "val": None, "varkind": None, "type": None}  # 表达式的属性（运算符，数值，变量类型，检查类型）
        }

    def setchild(self):
        self.child = [TreeNode(), TreeNode(), TreeNode()]

    def setchild1(self):
        self.child[1] = TreeNode()

    def setchild0(self):
        self.child[0] = TreeNode()

    def setchild2(self):
        self.child[2] = TreeNode()

    def setbro(self):
        self.brother = TreeNode()


def copyTreeNode(a, b):
    if b.brother != None:
        a.brother = b.brother
    if b.child[0] != None:
        a.child[0] = b.child[0]
    if b.child[1] != None:
        a.child[1] = b.child[1]
    if b.child[2] != None:
        a.child[2] = b.child[2]
    if b.line != 0:
        a.line = b.line
    if b.nodekind != None:
        a.nodekind = b.nodekind
    a.kind = copy.copy(b.kind)
    a.idnum = b.idnum
    a.name = b.name
    a.table = b.table
    a.type_name = b.type_name
    a.attr = copy.copy(b.attr)
    return a


# 节点类型
class NodeKind(Enum):
    ProK = 1  # 根标志
    PheadK = 2  # 程序头标志节点
    TypeK = 3  # 类型声明标志
    VarK = 4  # 变量声明标志
    ProcDecK = 5  # 函数声明标志
    StmLK = 6  # 语句标志节点
    DecK = 7  # 声明节点
    StmtK = 8  # 语句节点
    ExpK = 9  # 表达式节点


# 声明类型
class DecKind(Enum):
    ArrayK = 1  # 组类型
    CharK = 2  # 字符类型
    IntegerK = 3  # 整数类型
    RecordK = 4  # 记录类型
    IdK = 5  # 类型标识符


# 语句类型
class StmtKind(Enum):
    IfK = 1
    WhileK = 2
    AssignK = 3
    ReadK = 4
    WriteK = 5
    CallK = 6
    ReturnK = 7


# 表达式类型
class ExpKind(Enum):
    OpK = 1
    ConstK = 2
    VariK = 3  # 变量


# 变量类别
class VarKind(Enum):
    IdV = 1  # 标识符变量
    ArrayMembV = 2  # 数组成员变量
    FieldMembV = 3  # 域成员变量


# 节点的检查类型
class ExpType(Enum):
    Void = 1
    Integer = 2
    Boolean = 3


class ParamType(Enum):
    valparamType = 1  # 值参
    varparamType = 2  # 变参


class AccessKind(Enum):
    dir = 1
    indir = 2


# 标识符类别
class IdKind(Enum):
    typeKind = 1
    varKind = 2
    procKind = 3


class Token():
    def __init__(self, line=0, lex=LexType.DEFAULT, sem=None):
        self.line = line
        self.lex = lex
        self.sem = sem

    def setLine(self, line):
        self.line = line

    def setLex(self, lex):
        self.lex = lex

    def setSem(self, sem):
        self.sem = sem

    def getString(self):
        if self.sem != None:
            return "<" + str(self.line) + "," + self.lex.name + "," + str(self.sem) + ">"
        else:
            return "<" + str(self.line) + "," + self.lex.name + ">"


# 打印语法树
def printInLine(word):
    print(word, end="")  # 控制格式，避免一行没打印完换行


def printTab(num):
    i = 0
    while i < num:
        printInLine(" ")
        i += 1


def printTree(tree, indexNum):
    indexNum += 4  # 控制空白数
    while tree != None:
        if tree.line == 0:
            printTab(9)
        else:
            t = tree.line / 10
            printInLine("line:" + str(tree.line))
            if t == 0:
                printTab(0)
            elif t <= 9 and t >= 1:
                printTab(2)
            else:
                printTab(1)
        printTab(indexNum)

        if tree.nodekind == NodeKind.ProK:
            printInLine("Prok  ")
        elif tree.nodekind == NodeKind.PheadK:
            printInLine("PheadK  ")
            printInLine(tree.name[0] + "  ")
        elif tree.nodekind == NodeKind.DecK:
            printInLine("Deck  ")
            if tree.attr["ProcAttr"]["paramt"] == ParamType.varparamType:
                printInLine("var param:  ")
            if tree.attr["ProcAttr"]["paramt"] == ParamType.valparamType:
                printInLine("value param:  ")

            if tree.kind["dec"] == DecKind.ArrayK:
                printInLine("ArrayK  ")
                printInLine(str(tree.attr["ArrayAttr"]["up"]) + "  ")
                printInLine(str(tree.attr["ArrayAttr"]["low"]) + " ")
                if tree.attr["ArrayAttr"]["childtype"] == DecKind.CharK:
                    printInLine("Chark  ")
                elif tree.attr["ArrayAttr"]["childtype"] == DecKind.IntegerK:
                    printInLine("IntegerK  ")
            elif tree.kind["dec"] == DecKind.CharK:
                printInLine("Chark  ")
            elif tree.kind["dec"] == DecKind.IntegerK:
                printInLine("IntegerK  ")
            elif tree.kind["dec"] == DecKind.RecordK:
                printInLine("RecordK  ")
            elif tree.kind["dec"] == DecKind.IdK:
                printInLine("IdK  ")
                printInLine(tree.type_name + "  ")
            else:
                printInLine("error1!")

            if tree.idnum != 0:
                i = 0
                while i < tree.idnum:
                    printInLine(tree.name[i] + "  ")
                    i += 1
            else:
                printInLine("wrong!no var!\n")

        elif tree.nodekind == NodeKind.TypeK:
            printInLine("TypeK  ")

        elif tree.nodekind == NodeKind.VarK:
            printInLine("VarK  ")
            if tree.table[0] != None:
                printInLine(str(tree.table[0].attrIR["More"]["VarAttr"]["off"]) + "  " + \
                            str(tree.table[0].attrIR["More"]["VarAttr"]["level"]) + "  ")

        elif tree.nodekind == NodeKind.ProcDecK:
            printInLine("ProcDeck  ")
            printInLine(tree.name[0] + "  ")
            if tree.table[0] != None:
                printInLine(str(tree.table[0].attrIR["More"]["ProcAttr"]["mOff"]) + "  " + \
                            str(tree.table[0].attrIR["More"]["ProcAttr"]["nOff"]) + "  " + \
                            str(tree.table[0].attrIR["More"]["ProcAttr"]["nOff"]) + "  ")

        elif tree.nodekind == NodeKind.StmLK:
            printInLine("StmLK  ")

        elif tree.nodekind == NodeKind.StmtK:
            printInLine("StmtK  ")

            if tree.kind["stmt"] == StmtKind.IfK:
                printInLine("If  ")
            elif tree.kind["stmt"] == StmtKind.WhileK:
                printInLine("While  ")
            elif tree.kind["stmt"] == StmtKind.AssignK:
                printInLine("Assign  ")
            elif tree.kind["stmt"] == StmtKind.ReadK:
                printInLine("Read  ")
                printInLine(tree.name[0] + "  ")
                if tree.table[0] != None:
                    printInLine(str(tree.table[0].attrIR["More"]["VarAttr"]["off"]) + "  " + \
                                str(tree.table[0].attrIR["More"]["VarAttr"]["level"]) + "  ")
            elif tree.kind["stmt"] == StmtKind.WriteK:
                printInLine("Write  ")
            elif tree.kind["stmt"] == StmtKind.CallK:
                printInLine("Call  ")
                printInLine(tree.name[0] + "  ")
            elif tree.kind["stmt"] == StmtKind.ReturnK:
                printInLine("Return  ")
            else:
                printInLine("error2!")
        elif tree.nodekind == NodeKind.ExpK:
            printInLine("ExpK  ")
            if tree.kind["exp"] == ExpKind.OpK:
                printInLine("Op  ")
                if tree.attr["ExpAttr"]["op"] == LexType.EQ:
                    printInLine("=  ")
                elif tree.attr["ExpAttr"]["op"] == LexType.LT:
                    printInLine("<  ")
                elif tree.attr["ExpAttr"]["op"] == LexType.PLUS:
                    printInLine("+  ")
                elif tree.attr["ExpAttr"]["op"] == LexType.TIMES:
                    printInLine("*  ")
                elif tree.attr["ExpAttr"]["op"] == LexType.MINUS:
                    printInLine("-  ")
                elif tree.attr["ExpAttr"]["op"] == LexType.OVER:
                    printInLine("/  ")
                else:
                    printInLine("error3!")

                if tree.attr["ExpAttr"]["varkind"] == VarKind.ArrayMembV:
                    printInLine("ArrayMember  ")
                    printInLine(tree.name[0] + "  ")

            elif tree.kind["exp"] == ExpKind.ConstK:
                printInLine("Const  ")
                if tree.attr["ExpAttr"]["varkind"] == VarKind.IdV:
                    printInLine("Id  ")
                    printInLine(tree.name[0])
                elif tree.attr["ExpAttr"]["varkind"] == VarKind.FieldMembV:
                    printInLine("FieldMember  ")
                    printInLine(tree.name[0])
                elif tree.attr["ExpAttr"]["varkind"] == VarKind.ArrayMembV:
                    printInLine("ArrayMember  ")
                    printInLine(tree.name[0])
                else:
                    # printInLine(tree.attr["ExpAttr"]["varkind"])
                    printInLine("var type error!")

                printInLine(str(tree.attr["ExpAttr"]["val"]) + "  ")

            elif tree.kind["exp"] == ExpKind.VariK:
                printInLine("Vari  ")
                if tree.attr["ExpAttr"]["varkind"] == VarKind.IdV:
                    printInLine("Id  ")
                    printInLine(tree.name[0] + "  ")
                elif tree.attr["ExpAttr"]["varkind"] == VarKind.FieldMembV:
                    printInLine("FieldMember  ")
                    printInLine(tree.name[0])
                elif tree.attr["ExpAttr"]["varkind"] == VarKind.ArrayMembV:
                    printInLine("ArrayMember  ")
                    printInLine(tree.name[0])
                else:
                    printInLine("var type error!")

                if tree.table[0] != None:
                    printInLine(tree.table[0].attrIR["More"]["VarAttr"]["off"] + "  " + \
                                tree.table[0].attrIR["More"]["VarAttr"]["level"] + "  ")

            else:
                printInLine("error4!")

        # else:
        #     printInLine("error5!")

        printInLine("\n")

        i = 0
        while i < 3:
            printTree(tree.child[i], indexNum)
            i += 1

        tree = tree.brother
    indexNum -= 4

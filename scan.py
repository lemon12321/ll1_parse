#词法分析

import sys, os, pickle
from enum import Enum
from globals import LexType, Token


# 有限自动机状态集合
class StateType(Enum):
    START = 1         #开始状态
    INASSIGN = 2      #赋值状态
    INRANGE = 3       #数组下标界限状态
    INCOMMENT = 4     #注释状态
    INNUM = 5         #数字状态
    INID = 6          #标识符状态
    INCHAR = 7        #字符标志状态
    DONE = 8          #完成状态


#保留字集合
reservedWords = {
    "program": LexType.PROGRAM, "type": LexType.TYPE, "var": LexType.VAR, "procedure": LexType.PROCEDURE,
    "begin": LexType.BEGIN, "end": LexType.END, "array": LexType.ARRAY, "of": LexType.OF, "record": LexType.RECORD,
    "if": LexType.IF, "then": LexType.THEN, "else": LexType.ELSE, "fi": LexType.FI, "while": LexType.WHILE,
    "do": LexType.DO, "endwh": LexType.ENDWH, "read": LexType.READ, "write": LexType.WRITE, "return": LexType.RETURN,
    "integer": LexType.INTEGER, "char": LexType.CHAR}


#获取当前行的下一个字符
def getNextchar(line):
    global inlinePos
    if inlinePos < len(line):
        c = line[inlinePos]
        inlinePos = inlinePos + 1
        return c
    else:
        raise IndexError


#回退到前一个字符
def ungetNextchar():
    global inlinePos
    if inlinePos > 0:
        inlinePos = inlinePos - 1
    else:
        raise IndexError


#在保留字集合匹配保留字
def reservedLookup(word):
    if word in reservedWords.keys():
        return reservedWords[word]
    else:
        return LexType.ID


#打印token序列
def showTokenlist(list):
    for token in list:
        print(token.getString())


#取得Token
def getTokenlist(pos, line):
    global tokenList
    currentToken = Token()

    while inlinePos < len(line):
        tokenString = ""
        state = StateType.START
        is_error = False   #是否出现错误

        while state != StateType.DONE:
            save = True
            try:
                ch = getNextchar(line)
                if state == StateType.START:
                    if ch.isalpha():
                        state = StateType.INID
                    elif ch.isdigit():
                        state = StateType.INNUM
                    elif ch == ':':
                        state = StateType.INASSIGN
                    elif ch == '.':
                        state = StateType.INRANGE
                    elif ch == ' ' or ch == '\t' or ch == '\n':
                        save = False
                    elif ch == '{':
                        state = StateType.INCOMMENT
                        save = False
                    elif ch == '\'':    #单引号
                        save = False
                        state = StateType.INCHAR
                    else:
                        state = StateType.DONE
                        if inlinePos == len(line):
                            save = False
                        elif ch == '=':
                            currentToken.setLex(LexType.EQ)
                        elif ch == '+':
                            currentToken.setLex(LexType.PLUS)
                        elif ch == '-':
                            currentToken.setLex(LexType.MINUS)
                        elif ch == '*':
                            currentToken.setLex(LexType.TIMES)
                        elif ch == '/':
                            # currentToken.setLex(LexType.OVER)
                            currentToken.setLex(LexType.DIVIDE)
                        elif ch == '<':
                            currentToken.setLex(LexType.LT)
                        elif ch == '(':
                            currentToken.setLex(LexType.LPAREN)
                        elif ch == ')':
                            currentToken.setLex(LexType.RPAREN)
                        elif ch == '[':
                            currentToken.setLex(LexType.LMIDPAREN)
                        elif ch == ']':
                            currentToken.setLex(LexType.RMIDPAREN)
                        elif ch == ';':
                            currentToken.setLex(LexType.SEMI)
                        elif ch == ',':
                            currentToken.setLex(LexType.COMMA)
                        else:
                            currentToken.setLex(LexType.ERROR)
                            is_error = True
                elif state == StateType.INID:
                    if not ch.isalnum():
                        ungetNextchar()
                        save = False
                        state = StateType.DONE
                        currentToken.setLex(LexType.ID)
                elif state == StateType.INNUM:
                    if not ch.isdigit():
                        ungetNextchar()
                        save = False
                        state = StateType.DONE
                        currentToken.setLex(LexType.INTC_VAL)
                        # currentToken.setLex(LexType.INTC)
                elif state == StateType.INASSIGN:
                    if ch == '=':
                        state = StateType.DONE
                        currentToken.setLex(LexType.ASSIGN)
                    else:
                        ungetNextchar()
                        save = False
                        state = StateType.DONE
                        currentToken.setLex(LexType.ERROR)
                        is_error = True
                elif state == StateType.INCOMMENT:
                    save = False
                    if inlinePos == len(line) - 1:
                        state = StateType.DONE
                    elif ch == '}':
                        state = StateType.START
                elif state == StateType.INRANGE:
                    state = StateType.DONE
                    if ch == '.':
                        # currentToken.setLex(LexType.UNDERANGE)
                        currentToken.setLex(LexType.UNDERRANGE)
                    else:
                        ungetNextchar()
                        save = False
                        currentToken.setLex(LexType.DOT)
                elif state == StateType.INCHAR:
                    if ch.isalnum():
                        cch = getNextchar()
                        if cch == '\'':
                            save = True
                            state = StateType.DONE
                            currentToken.setLex(LexType.CHARC_VAL)
                        else:
                            ungetNextchar()
                            ungetNextchar()
                            state = StateType.DONE
                            currentToken.setLex(LexType.ERROR)
                            is_error = True
                    else:
                        ungetNextchar()
                        state = StateType.DONE
                        currentToken.setLex(LexType.ERROR)
                        is_error = True
                else:
                    state = StateType.DONE
                    currentToken.setLex(LexType.ERROR)
                    is_error = True

                if save:
                    tokenString = tokenString + ch

            except IndexError:
                break

        if is_error:
            print("error in line " + str(linePos) + "  \"" + tokenString + "\"")

        currentToken.setLine(pos)
        if currentToken.lex == LexType.ID:
            currentToken.setLex(reservedLookup(tokenString))
            if currentToken.lex == LexType.ID:
                currentToken.setSem(tokenString)
        else:
            currentToken.setSem(tokenString)

        if tokenString != '':
            tokenList.append(currentToken)
            currentToken = Token()




if __name__ == '__main__':
    global theCodeArray, inlinePos, linePos, tokenList, scanToken
    inlinePos = 0   #一行的索引
    linePos = 0      #行数
    tokenList = []    #存token序列
    scanToken = "tokenList.data"             #生成的token序列要保存成的数据文件

    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        if not os.path.isfile(fileName):
            print("Please check the filename")         #若不是文件名的情况，出错
            exit(-1)
    else:
        print("argv is wrong")                   #终端执行时提供的参数数目不对，应该第一个是本程序文件名，第二个是要编译的文件名
        exit(-2)

    file = open(fileName)
    theCodeArray = file.readlines()           #按行读取文件，一项为一行
    file.close()

    for line in theCodeArray:
        inlinePos = 0
        linePos = linePos + 1
        if not '\n' in line:         #若一行中没有回车就加上，避免在生成token序列时标志出错
            line += '\n'
        getTokenlist(linePos,line)       #逐行生成token序列

    currentToken = Token(linePos + 1, LexType.ENDFILE, None)
    tokenList.append(currentToken)   #加入文件结尾的EOF

    showTokenlist(tokenList)   #打印生成的token序列

    if not os.path.isdir("record"):
        os.mkdir("record")           #创建目录
    os.chdir("record")             #指定工作目录
    fp = open(scanToken,'wb')
    pickle.dump(tokenList,fp)         #将token序列序列化保存到data数据文件中
    fp.close()
    os.chdir("..")                   #跳转回项目工作路径


    # #只是为了看数据读取是不是成功，可省略
    # os.chdir("record")                 #跳转到record目录读取数据
    # fp = open(scanToken,'rb')
    # tokenList2 = pickle.load(fp)        #将data数据解析为对象
    # fp.close()
    # print("token is:")
    # showTokenlist(tokenList2)
    # os.chdir("..")











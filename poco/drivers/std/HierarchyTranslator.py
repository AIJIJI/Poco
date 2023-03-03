from poco.global_state import *


class TranslatorAgent(object):
    blockAttrs = []
    OptimizeDataEnabled = True

    def SetOptimizeDataEnabled(self, enabled):
        self.OptimizeDataEnabled = enabled

    def SetBlockAttrs(self, *args):
        self.blockAttrs = []
        for arg in args:
            self.blockAttrs.append(arg)

    def GetMatchingBracket(self, leftBracket, m_str, start, end):
        stack = Stack()

        rightBracket = ''
        if leftBracket == '{':
            rightBracket = '}'
        elif leftBracket == '[':
            rightBracket = ']'
        elif leftBracket == '\"':
            rightBracket = '\"'
        else:
            raise Exception("GetMatchingBracket: invalid left bracket")

        matchingInd = start
        stack.push(leftBracket)

        for i in range(start, end):
            c = m_str[i]
            if stack.size() > 0 and stack.peek() == '\"':
                if c == '\"':
                    stack.pop()
                    if leftBracket == '\"' and stack.size() == 0: return i;
                continue
            if c == '\"':
                stack.push(c)
            if c == leftBracket:
                stack.push(c)
            if c == rightBracket:
                stack.pop()
            if stack.size() == 0:
                matchingInd = i
                break

        return matchingInd

    leftSymbol = ['\"', '[', '{']

    def SplitItemByComma(self, m_str, start, end):
        strList = []

        leftPtr = start
        rightPtr = leftPtr
        jump = False

        i = start
        while i < end:
            stri = m_str[i]
            if jump == False and self.leftSymbol.__contains__(stri):
                j = self.GetMatchingBracket(stri, m_str, i + 1, end)
                jump = True
                i = j
                continue
            if jump: jump = False

            if stri == ',':
                rightPtr = i
                itemStr = m_str[leftPtr:rightPtr]
                strList.append(itemStr)
                leftPtr = i + 1

            if i == end - 1:
                rightPtr = i + 1
                itemStr = m_str[leftPtr:rightPtr]
                strList.append(itemStr)

            i = i + 1
        return strList

    def TrimQuatation(self, m_str):
        valid = False
        if m_str[0] == '\\' and m_str[1]=='\"' and m_str[len(m_str) - 2] == '\\' and m_str[len(m_str) - 1] == '\"':
            valid = True
            return m_str[1: len(m_str) - 3]
        if m_str[0] == '\"' and m_str[len(m_str) - 1] == '\"':
            valid = True
            return m_str[1: len(m_str) - 1]

        if valid == False:
            print("TrimQuatation: " + m_str)
            print("!!!!!!!!!!!!!!!!!!!!!!!!! TrimQuatation Invalid Str")
            raise Exception("TrimQuatation::Invalid str")


    def StrToBool(self, m_str):
        if m_str == "\\\"True\\\"": return True
        if m_str == "\"True\"": return True
        if m_str == "\\\"False\\\"": return False
        if m_str == "\"False\"": return False
        print("StrToBool: " + m_str)
        print("!!!!!!!!!!!!!!!!!!!!!!!!! StrToBool Invalid Str")
        raise Exception("StrToBool::Invalid str")

    def StrToFloatArr(self, m_str):
        #if m_str!="[0,0]" and m_str!="[0.5,0.5]" :
        #    print("StrToFloatArr" + str(m_str))
        tmp = m_str[1: len(m_str) - 1]
        tmpArr = tmp.split(',')
        n1 = float(tmpArr[0])
        n2 = float(tmpArr[1])
        arr = [n1, n2]
        return arr

    def StrToZOrdersDic(self, m_str):
        tmp = m_str[1: len(m_str) - 1]
        tmpArr = tmp.split(',')
        n1 = float(tmpArr[0])
        n2 = float(tmpArr[1])
        arr = [n1, n2]
        dic = dict()
        dic["global"] = n1
        dic["local"] = n2
        return dic

    def Translate(self, raw_data):
        #print("Data Optimize Mode: " + str(self.OptimizeDataEnabled))
        if self.OptimizeDataEnabled == False:
            return raw_data

        try:
            res = self.Translate_internal(raw_data)
        except BaseException as e:
            if UWA_POCO_DEBUG:
                print("Translate using OptimizeData mode failed, set OptimizeDataEnabled to false")
                print(str(e))
                import traceback
                info = traceback.format_exc()
                print(info)
            res = raw_data
        return res

    def Translate_internal(self, raw_data):

        result = ""
        if raw_data == "": return ""
        nodeDic = dict()
        left = "{{"
        payloadStart = 2
        payloadEnd = self.GetMatchingBracket('{', raw_data, 2, len(raw_data))
        payloadList = self.SplitItemByComma(raw_data, payloadStart, payloadEnd)
        payloadDic = dict()
        attrCnt = 0
        if not self.blockAttrs.__contains__("name"):
            payloadDic["name"] = self.TrimQuatation(payloadList[attrCnt])
            attrCnt= attrCnt+1
        if not self.blockAttrs.__contains__("visible"):
            payloadDic["visible"] = self.StrToBool(payloadList[attrCnt])
            attrCnt= attrCnt+1
        if not self.blockAttrs.__contains__("pos"):
            payloadDic["pos"] = self.StrToFloatArr(payloadList[attrCnt])
            attrCnt= attrCnt+1
        if not self.blockAttrs.__contains__("size"):
            payloadDic["size"] = self.StrToFloatArr(payloadList[attrCnt])
            attrCnt= attrCnt+1
        if not self.blockAttrs.__contains__("anchorPoint"):
            payloadDic["anchorPoint"] = self.StrToFloatArr(payloadList[attrCnt])
            attrCnt= attrCnt+1
        if not self.blockAttrs.__contains__("zOrders"):
            payloadDic["zOrders"] = self.StrToZOrdersDic(payloadList[attrCnt])
            attrCnt= attrCnt+1

        if not self.blockAttrs.__contains__("text"):
            textStr = self.TrimQuatation(payloadList[attrCnt])
            if not (textStr == None or len(textStr) == 0):
                payloadDic["text"] = textStr
            attrCnt = attrCnt + 1

        if not self.blockAttrs.__contains__("texture"):
            texStr = self.TrimQuatation(payloadList[attrCnt])
            if not (texStr == None or len(texStr) == 0):
                payloadDic["texture"] = texStr
            attrCnt= attrCnt+1

        if not self.blockAttrs.__contains__("_instanceId"):
            tmp = payloadList[attrCnt]
            if not (tmp == None or len(tmp) == 0):
                payloadDic["_instanceId"] = int(tmp)
            attrCnt= attrCnt+1

        nodeDic["name"] = self.TrimQuatation(payloadList[0])
        nodeDic["payload"] = payloadDic
        #print(str(nodeDic["payload"]))

        if payloadEnd == len(raw_data) - 1 - 1: return nodeDic

        valid = False
        if raw_data[payloadEnd + 1] == ',' and raw_data[payloadEnd + 2] == '[':
            valid = True

        if valid == False: raise Exception("Invalid str")

        childrenStart = payloadEnd + 3
        childrenEnd = len(raw_data) - 2

        childrenStrList = self.SplitItemByComma(raw_data, childrenStart, childrenEnd)
        childList = []
        for i in range(0, len(childrenStrList)):
            childList.append(self.Translate_internal(childrenStrList[i]))

        if len(childList) != 0: nodeDic["children"] = childList

        return nodeDic

        return result


translator_agent = TranslatorAgent()

class Stack(object):
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


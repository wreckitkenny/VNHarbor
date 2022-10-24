import urllib.parse

def doubleEncode(string):
    encodedStr = urllib.parse.quote(string, safe='')
    encodedStr = urllib.parse.quote(encodedStr, safe='')
    return encodedStr

def doubleDecode(encoded):
    decodedStr = urllib.parse.unquote(encoded)
    decodedStr = urllib.parse.unquote(decodedStr)
    return decodedStr

def getPageEncoding():
    return 'utf8'
    
def translateToPageEncoding(s):
    try:
        return s.encode(getPageEncoding())
    except:
        return "encoding error"+s.encode(getPageEncoding(), 'backslashreplace')
        
def decodeToUnicode(s):
    if type(s) == unicode:
        return s
    try:
        return s.decode(getPageEncoding())
    except:
        return "decoding error"+s.encode(getPageEncoding(), 'backslashreplace')

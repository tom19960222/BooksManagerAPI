# Solution from: http://stackoverflow.com/questions/379906/parse-string-to-float-or-int
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
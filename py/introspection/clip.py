
def clip(text: str, max_len: 'int > 0' = 80) -> str:
    '''
    Return the text clipped at the last space before or after mak_len
    :param text: text to be clipped
    :param max_len: maximum length of the string; default is 80
    :return: return a clipped text
    '''
    
    end = None
    if len(text) > max_len:
            space_before = text.rfind(' ', 0, max_len)
            if space_before >= 0:
                end  = space_before
            else:
                space_after = text.rfind(' ', max_len)
                if space_after >= 0:
                    end = space_after
    if end is None:     # no spaces were found
        end = len(text)
    return text[:end].rstrip

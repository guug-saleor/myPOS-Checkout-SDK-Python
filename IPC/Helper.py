class Helper():

    _escapes = {
        ord('&'): '&amp;',
        ord('<'): '&lt;',
        ord('>'): '&gt;',
        ord('"'): '&quot;',
        ord("'"): '&#39;',
    }

    def __init__(self):
        pass

    @classmethod
    def escape(cls, text):
        return str(cls.unescape(text)).translate(cls._escapes)

    @classmethod
    def unescape(cls, text):
        return text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
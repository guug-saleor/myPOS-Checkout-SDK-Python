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

    def escape(self, text):
        return str(self.unescape(text)).translate(_escapes)

    def unescape(self, text):
        return text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
# -*- coding: utf-8 -*-

class Error(Exception):
    pass

class ESError(Error):
    pass

class ESConnectionError(ESError, IOError):
    pass

class ESRequestError(ESError, ValueError):
    pass
#     def __init__(self, status, msg):
#         self.status = status
#         self.msg = msg
#     
#     def __str__(self):
#         return "(%s, %s)" % (self.status, self.msg)
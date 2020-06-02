# How to add a new parser
The parser file must contain either of the following:
1. A class with a method `parse` with the signature (self, context, snapshot)
2.  A method that begins with `parse_`, for example `parse_feelings` and has the signature (context, snapshot).

Either way, it should return a dict, the keys for the dict will be the values that will be saved via the saver.


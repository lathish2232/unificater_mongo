import json


class ErrorProperties():

    def __init__(self, node_id=None, clause_id=None, column_id=None, msg=None):
        self.__node_id = node_id
        self.__clause_id = clause_id
        self.__column_id = column_id
        self.__msg = msg

    def get_node_id(self):
        return self.__node_id

    def set_node_id(self, node_id):
        self.__node_id = node_id

    def get_clause_id(self):
        return self.__clause_id

    def set_clause_id(self, clause_id):
        self.__clause_id = clause_id

    def get_column_id(self):
        return self.__column_id

    def set_column_id(self, column_id):
        self.__column_id = column_id

    def get_msg(self):
        return self.__msg

    def set_msg(self, msg):
        self.__msg = msg

    def json_str(self):
        errro_msg = {"Node": self.__node_id, "Clause": self.__clause_id, "Column": self.__column_id,
                     "Error": self.__msg}
        return json.dumps(errro_msg)

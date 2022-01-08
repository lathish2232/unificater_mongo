import json

from pandas import DataFrame

import service.impl.refpkg.merge as uni
from service.util import node_utils
from service.util.json_utils import extract_sub_json
from service.util.query_builder_property import ErrorProperties
from service.util.unify_logger import unify_printer


class Query:
    col_list = None
    qbuilder_property = ErrorProperties()

    def __init__(self, json, flow, node_id):
        self.df = DataFrame()
        self.json = json
        self.flow = flow
        self.node_id = node_id
        self.label_path = f'/{self.flow}/nodes/{self.node_id}/data/label'
        self.node_path = f'/{self.flow}/nodes/{self.node_id}/data/query'
        self.clause_list = extract_sub_json(self.node_path + '/clauses', self.json)[3]
        self.clause_json = self.clause_list

        Query.json = json
        Query.flow = flow
        Query.node_id = node_id
        Query.label_path = f'/{Query.flow}/nodes/{Query.node_id}/data/label'
        Query.node_path = f'/{Query.flow}/nodes/{Query.node_id}/data/query'
        Query.clause_list = extract_sub_json(Query.node_path + '/clauses', Query.json)[3]
        Query.clause_json = Query.clause_list

        # Query.label_path = self.label_path
        # Query.node_path = self.node_path
        # Query.clause_list = self.clause_list

    # df = DataFrame()
    # json = json
    # flow = flow
    # node_id = node_id
    # clause_json = json
    # label_path = f'/{flow}/nodes/{node_id}/data/label'
    # node_path = f'/{flow}/nodes/{node_id}/data/query'
    # clause_list = extract_sub_json(node_path + '/clauses', json)[3]

    def clauses(self):
        self.qbuilder_property.set_node_id(self.node_id)
        clause_idx = 0
        for clause in self.clause_list:
            self.qbuilder_property.set_clause_id(clause.get('id'))
            clause_id = clause.get('id')
            clause_type = clause.get('type')
            self.clause_json = clause
            if clause_type == 'select':
                clause_func = self.select_clause
            elif clause_type == 'groupBy':
                clause_func = self.group_by_clause
            elif clause_type == 'orderBy':
                clause_func = Query.order_by_clause
            elif clause_type == 'where':
                clause_func = self.where_clause
            elif clause_type == 'join':
                clause_func = self.join_clause
            elif clause_type == 'union':
                clause_func = Query.union_clause
            else:
                pass
                unify_printer(message=f"Invalid Clause type '{type}'.")
            clause_idx += 1
        df = clause_func(Query.flow, Query.node_id, clause_id, clause_idx - 1)  # Need to change this in the prod build
        self.qbuilder_property.set_clause_id(None)
        self.qbuilder_property.set_column_id(None)
        return df

    def run_data_item(self, flow, node_id, clause_idx=None, parent=True):
        data = []
        if parent:
            cidx = clause_idx - 1
        else:
            cidx = clause_idx
        if cidx >= 0:
            clause_type = self.clause_list[cidx]['type']
            clause_id = self.clause_list[cidx]['id']
            if clause_type == 'select':
                # df=self.select_clause(flow, node_id, clause_id, clause_idx)
                data.append(
                    {"func": self.select_clause, "node_id": node_id, "clause_id": clause_id, "clause_idx": cidx})
            elif clause_type == 'groupBy':
                # df=self.group_by_clause(flow, node_id, parent_clause_id, clause_idx)
                data.append(
                    {"func": self.group_by_clause, "node_id": node_id, "clause_id": clause_id, "clause_idx": cidx})
            elif clause_type == 'orderBy':
                # df=self.order_by_clause(flow, node_id, parent_clause_id, clause_idx)
                data.append(
                    {"func": self.order_by_clause, "node_id": node_id, "clause_id": clause_id, "clause_idx": cidx})
            elif clause_type == 'where':
                # df=self.where_clause(flow, node_id, parent_clause_id, clause_idx)
                data.append({"func": self.where_clause, "node_id": node_id, "clause_id": clause_id, "clause_idx": cidx})
            elif clause_type == 'join':
                # df=self.join_clause(flow, node_id, parent_clause_id, clause_idx)
                data.append({"func": self.join_clause, "node_id": node_id, "clause_id": clause_id, "clause_idx": cidx})
            elif clause_type == 'union':
                # df=self.union_clause(flow, node_id, parent_clause_id, clause_idx)
                data.append({"func": self.union_clause, "node_id": node_id, "clause_id": clause_id, "clause_idx": cidx})
            else:
                pass
                unify_printer(message=f"Invalid Clause type '{clause_type}'.")
            # return df
        else:
            if parent:
                for _, parent in self.json.get(flow).get('nodes').get(node_id).get('data').get('parents').items():
                    type = parent['type']
                    parent_id = parent['id']
                    if type == 'sourceNode':
                        data.append({"func": node_utils.source_node, "node_id": parent_id})
                    elif type == 'joinNode':
                        data.append({"func": node_utils.join_node, "node_id": parent_id})
                    elif type == 'unionNode':
                        data.append({"func": node_utils.union_node, "node_id": parent_id})
                    elif type == 'dataInstance':
                        inst_id = parent['instanceId']
                        data_inst_id = parent['id']
                        data.append(
                            {"func": node_utils.data_instance, "inst_id": inst_id, "data_inst_id": data_inst_id})
            else:
                type = self.json.get(flow).get('nodes').get(node_id).get('data').get('type')
                if type == 'sourceNode':
                    data.append({"func": node_utils.source_node, "node_id": node_id})
                elif type == 'joinNode':
                    data.append({"func": node_utils.join_node, "node_id": node_id})
                elif type == 'unionNode':
                    data.append({"func": node_utils.union_node, "node_id": node_id})
        return data

    # @lru()
    @classmethod
    def select_clause(cls, flow, node_id, clause_id, clause_idx):
        try:
            aliases = []
            records = cls.clause_list[clause_idx]['columns']
            clause_df = node_id

            data = cls.run_data_item(cls, flow, node_id, clause_idx)[0]
            func = data.pop('func')

            exec(f"{clause_df}=func(flow, **data)")
            # if clause_idx == 0:
            #     data=cls.run_data_item(cls, flow, node_id)[0]
            #     func=data.pop('func')
            #     exec(f"{clause_df}=func(flow, **data)")
            # else:
            #     exec(f"{clause_df}=cls.run_data_item(cls, flow, node_id, clause_idx-1)")
            if records:
                for rec in records:
                    cls.qbuilder_property.set_column_id(rec.get('id'))
                    if not rec['disabled']:
                        alias = rec['alias']
                        exec(f"{clause_df}['{alias}']=" + rec['expression'])
                        aliases.append(alias)
                        if rec.get('window') and rec.get('isWindowApplied'):
                            exec(cls.window_function(cls, clause_df, alias, rec['window']))
                eval(clause_df).drop(columns=eval(f"{clause_df}.columns.difference({aliases})"), inplace=True)
                # Fetch Distinct data
                # distinct = extract_sub_json(cls.node_path + '/distinct', cls.json)[3]
                # if distinct:
                #     eval(clause_df).drop_duplicates(inplace=True)
                # #Fetch limited rows
                # n_rows = extract_sub_json(cls.node_path + '/noOfRecords', cls.json)[3]
                # if n_rows['sortBy'] == 'From Top':
                #     exec(f"{clause_df}={clause_df}.head(int(n_rows['records'])")
                #     #cls.df = cls.df.head(int(n_rows['records']))
                # elif n_rows['sortBy'] == 'From Bottom':
                #     exec(f"{clause_df}={clause_df}.tail(int(n_rows['records'])")
                #     #cls.df = cls.df.tail(int(n_rows['records']))
                # else:
                #     exec(f"{clause_df}={clause_df}.sample(int(n_rows['records'])")
                #     #cls.df = cls.df.sample(int(n_rows['records']))

        except Exception as ex:
            ex = str(ex).replace('name', 'Column')
            cls.qbuilder_property.set_msg(ex)
            raise
        return eval(clause_df)

    def distinct(self):
        try:
            distinct = extract_sub_json(self.node_path + '/distinct', self.json)[3]
            if distinct:
                self.df = self.df.drop_duplicates()
        except Exception as ex:
            self.qbuilder_property.set_msg(ex)
        return self.df

    def no_of_record(self):
        try:
            n_rows = extract_sub_json(self.node_path + '/noOfRecords', self.json)[3]
            if n_rows['sortBy'] == 'From Top':
                self.df = self.df.head(int(n_rows['records']))
            elif n_rows['sortBy'] == 'From Bottom':
                self.df = self.df.tail(int(n_rows['records']))
            else:
                self.df = self.df.sample(int(n_rows['records']))
        except Exception as ex:
            self.qbuilder_property.set_msg(ex)
        n_rows = extract_sub_json(self.node_path + '/noOfRecords', self.json)[3]
        if n_rows['records']:
            if n_rows['sortBy'] == 'From Top':
                self.df = self.df.head(int(n_rows['records']))
            elif n_rows['sortBy'] == 'From Bottom':
                self.df = self.df.tail(int(n_rows['records']))
            else:
                self.df = self.df.sample(int(n_rows['records']))
        return self.df

    # @lru()
    @classmethod
    def where_clause(cls, flow, node_id, clause_id, clause_idx):
        try:
            condition = ""
            clause_df = node_id
            data = cls.run_data_item(cls, flow, node_id, clause_idx)[0]
            func = data.pop('func')
            exec(f"{clause_df}=func(flow, **data)")

            # if clause_idx == 0:
            #     data=cls.run_data_item(cls, flow, node_id)[0]
            #     func=data.pop('func')
            #     exec(f"{clause_df}=func(flow, **data)")
            # else:
            #     exec(f"{clause_df}=cls.run_data_item(cls, flow, node_id, clause_idx)")

            def condition_builder(conditions_dict, condition):
                for con in conditions_dict:
                    cls.qbuilder_property.set_column_id(con.get('id'))
                    if con["isnot"]:
                        condition += "~"
                    if con["groupOf"]:
                        condition += f'({condition_builder(con["groupOf"], "")})'
                    op = ""
                    if con["conditionalOperator"] == "AND":
                        op = " & "
                    elif con["conditionalOperator"] == "OR":
                        op = " | "
                    else:
                        op = ""
                    if con["condition"]:
                        # logging.info(con["condition"])
                        lhs_expression = con["condition"]["LHS"]
                        rhs_expression = con["condition"]["RHS"]
                        rhs_exp = rhs_expression
                        lhs_exp = lhs_expression
                        if con["condition"]["operator"] == "=":
                            cont = f'({lhs_exp} == {rhs_exp})'
                        elif con["condition"]["operator"] == "!=":
                            cont = f'({lhs_exp} != {rhs_exp})'
                        elif con["condition"]["operator"] == ">":
                            cont = f'({lhs_exp} > {rhs_exp})'
                        elif con["condition"]["operator"] == "<":
                            cont = f'({lhs_exp} < {rhs_exp})'
                        elif con["condition"]["operator"] == ">=":
                            cont = f'({lhs_exp} >={rhs_exp})'
                        elif con["condition"]["operator"] == "<=":
                            cont = f'({lhs_exp} <= {rhs_exp})'
                        elif con["condition"]["operator"].upper() == "STARTS WITH":
                            cont = f'({lhs_exp}.str.startswith({rhs_exp}))'
                        elif con["condition"]["operator"].upper() == "NOT STARTS WITH":
                            cont = f'(~{lhs_exp}.str.startswith({rhs_exp}))'
                        elif con["condition"]["operator"].upper() == "ENDS WITH":
                            cont = f'({lhs_exp}.str.endswith({rhs_exp}))'
                        elif con["condition"]["operator"].upper() == "NOT ENDS WITH":
                            cont = f'(~{lhs_exp}.str.endswith({rhs_exp}))'
                        elif con["condition"]["operator"].upper() == "IN":
                            cont = f'({lhs_exp}.isin({rhs_exp}))'
                        elif con["condition"]["operator"].upper() == "NOT IN":
                            cont = f'(~{lhs_exp}.isin({rhs_exp}))'
                        elif con["condition"]["operator"].upper() == "IS NULL":
                            cont = f'{lhs_expression}.isnull()'
                        elif con["condition"]["operator"].upper() == "IS NOT NULL":
                            cont = f'{lhs_expression}.notnull()'
                        else:
                            operator = con["condition"]["operator"]
                            cont = f'({lhs_exp} {operator} {rhs_exp})'
                        condition += f'{cont}{op}'
                return condition

            conditions_dict = extract_sub_json(f'/{clause_id}/columns', cls.clause_json)[3]
            if conditions_dict:
                results = f"{clause_df}={clause_df}[{condition_builder(conditions_dict, condition)}]"
                exec(results)
        except Exception as ex:
            ex = str(ex).replace('name', 'Column')
            cls.qbuilder_property.set_msg(ex)
            raise
        return eval(f"{clause_df}")

    # @lru()
    @classmethod
    def group_by_clause(cls, flow, node_id, clause_id, clause_idx):
        try:
            groupBy = []
            select_groups = {}
            clause_json = cls.clause_json
            clause_df = node_id
            data = cls.run_data_item(cls, flow, node_id, clause_idx)[0]
            func = data.pop('func')
            exec(f"{clause_df}=func(flow, **data)")
            # if clause_idx == 0:
            #     data=cls.run_data_item(cls, flow, node_id)[0]
            #     func=data.pop('func')
            #     exec(f"{clause_df}=func(flow, **data)")
            # else:
            #     exec(f"{clause_df}=cls.run_data_item(cls, flow, node_id, clause_idx)")

            for rec in extract_sub_json(f'/{clause_id}/columns', clause_json)[3]:
                cls.qbuilder_property.set_column_id(rec.get('id'))
                if not rec['disabled']:
                    exp = rec['expression'].split('.')[-1]
                    groupBy.append(exp)

            grouping = eval(f'{clause_df}.groupby(groupBy)')
            for rec in extract_sub_json(f'/{clause_id}/selectGroups', clause_json)[3]:
                if not rec['disabled']:
                    cls.qbuilder_property.set_column_id(rec.get('id'))
                    exp = rec['expression'].split('.')[-1]
                    select_groups[exp] = rec['agg']

            df = grouping.agg(select_groups)
            df.columns = ['_'.join(col) for col in df.columns.values]
            df.reset_index(inplace=True)
            df.columns = cls.column_uniquify(df.columns)
        except ValueError as ex:
            if ValueError:
                ex = str(ex).replace('name', 'Column')
                cls.qbuilder_property.set_msg(
                    "No column selected in Group By,if Group by is empty please Remove from Query")
            else:
                ex = str(ex).replace('name', 'Column')
                cls.qbuilder_property.set_msg(ex)
            raise
        return df

    # @lru()
    @classmethod
    def order_by_clause(cls, flow, node_id, clause_id, clause_idx):
        # try:
        if True:
            orderby = []
            ascending = []
            clause_json = cls.clause_list[clause_idx]
            clause_df = node_id
            data = cls.run_data_item(cls, flow, node_id, clause_idx)[0]
            func = data.pop('func')
            exec(f"{clause_df}=func(flow, **data)")
            # if clause_idx == 0:
            #     data=cls.run_data_item(cls, flow, node_id, clause_idx)[0]
            #     func=data.pop('func')
            #     exec(f"{clause_df}=func(flow, **data)")
            # else:
            #     exec(f"{clause_df}=cls.run_data_item(cls, flow, node_id, clause_idx)")
            records = clause_json.get('columns')
            if records:
                for rec in records:
                    cls.qbuilder_property.set_column_id(rec.get('id'))
                    if not rec['disabled']:
                        exp = rec['expression'].split('.')[-1]
                        orderby.append(exp)
                        if rec['sortOrder'] == 'ASC':
                            ascending.append(True)
                        else:
                            ascending.append(False)
                exec(f"{clause_df}.sort_values(by=orderby, ascending=ascending, ignore_index=True, inplace=True)")

        # except Exception as ex:
        #     ex = str(ex).replace('name', 'Column')
        #     cls.qbuilder_property.set_msg(ex)
        #     raise
        return eval(f"{clause_df}")

    # @lru()
    @classmethod
    def join_clause(cls, flow, node_id, clause_id, clause_idx):

        left_condition = []
        right_condition = []
        join = {}

        def get_join(how):
            join = ""
            if how.get('left'):
                join = join + 'L'
            if how.get('middle'):
                join = join + 'M'
            if how.get('right'):
                join = join + 'R'
            return join

        data_list = cls.run_data_item(cls, flow, node_id, clause_idx)
        parent_ids = []
        for i, data in enumerate(data_list):
            parent_id = data['node_id']
            keys: list = [key for key in cls.json.get(flow).get('nodes').keys() if key.endswith('-link')]
            for key in keys:
                # if key.endswith('-link'):
                target = cls.json.get(flow).get('nodes').get(key).get('target')
                source = cls.json.get(flow).get('nodes').get(key).get('source')
                if node_id == target and parent_id == source:
                    plug = cls.json.get(flow).get('nodes').get(key).get('targetHandle').split('-')[-1]
                    join[plug] = data.get('func')
                    parent_ids.append(parent_id)
                    break
        # try:
        if True:
            clause_json = cls.clause_json[clause_idx]
            how = clause_json.get('how')
            conditions = clause_json.get('conditions')
            if conditions or len(left_condition) > 0:
                for condition in conditions:
                    left_condition.append(condition.get('LHS').get('name'))
                    right_condition.append(condition.get('RHS').get('name'))
            join_cnd = get_join(how)
            left_df = DataFrame(join.get('left')(flow, parent_ids[0]))
            right_df = DataFrame(join.get('right')(flow, parent_ids[1]))
            if join_cnd == 'L':
                result = uni.merge(left_df, right_df, how="outer",
                                   left_on=left_condition, right_on=right_condition, indicator=True).query(
                    '_merge=="left_only"')  # LEFT OUTER JOIN - Matched in LEFT NOT MIDDLE
            elif join_cnd == 'R':
                result = uni.merge(left_df, right_df, how="outer",
                                   left_on=left_condition, right_on=right_condition, indicator=True).query(
                    '_merge=="right_only"')  # RIGHT OUTER JOIN - Matched in RIGHT NOT MIDDLE
            elif join_cnd == 'M':
                result = uni.merge(left_df, right_df, how='inner',
                                   left_on=left_condition,
                                   right_on=right_condition)  # INNER JOIN - Matched in LEFT & RIGHT
            elif join_cnd == 'LM':
                result = uni.merge(left_df, right_df, how='left',
                                   left_on=left_condition,
                                   right_on=right_condition)  # LEFT JOIN - Matched in LEFT & MIDDLE
            elif join_cnd == 'MR':
                result = uni.merge(left_df, right_df, how='right',
                                   left_on=left_condition,
                                   right_on=right_condition)  # RIGHT JOIN - Matched in RIGHT & MIDDLE
            elif join_cnd == 'LR':
                left = uni.merge(left_df, right_df, how="outer",
                                 left_on=left_condition, right_on=right_condition, indicator=True).query(
                    '_merge=="left_only"')  # LEFT OUTER JOIN - Matched in LEFT NOT MIDDLE
                right = uni.merge(left_df, right_df, how="outer",
                                  left_on=left_condition, right_on=right_condition, indicator=True).query(
                    '_merge=="right_only"')  # RIGHT OUTER JOIN - Matched in RIGHT NOT MIDDLE
                result = uni.merge(left, right, how='outer', left_on=left_condition,
                                   right_on=right_condition)  # RIGHT JOIN - Matched in LEFT, RIGHT & MIDDLE
            elif join_cnd == 'LMR':
                result = uni.merge(left_df, right_df, how='outer',
                                   left_on=left_condition,
                                   right_on=right_condition)  # RIGHT JOIN - Matched in LEFT, RIGHT & MIDDLE
            else:
                result = uni.merge(left_df, right_df, how='cross')  # INNER JOIN - Matched in LEFT & RIGHT
        # except Exception as ex:
        #     ex = str(ex).replace('name', 'Column')
        #     cls.qbuilder_property.set_msg(ex)
        return result

    # @lru()
    @classmethod
    def union_clause(cls, flow, node_id, clause_id, clause_idx):
        result = DataFrame()

        data_list = cls.run_data_item(cls, flow, node_id, clause_idx)
        try:
            for data in data_list:
                parent_id = data["node_id"]
                func = data.get('func')
                df=func(flow, parent_id)
                df["_NodeName_"]=parent_id
                result = result.append(df,ignore_index=True)
        except Exception as ex:
            ex = str(ex).replace('name', 'Column')
            cls.qbuilder_property.set_msg(ex)
            raise
        return result

    def window_function(self, df, column, winjson):
        group_by = winjson.get("groupBy")
        windowing = winjson.get("windowing")
        groupby_col = group_by
        function = winjson.get("function")
        win_type = windowing.get("type")
        wineval = f"{df}['{column}']={df}"
        if groupby_col:
            wineval += f".groupby(by={groupby_col})"
        wineval += f"['{column}']"
        if win_type.upper() == "NONE":
            if groupby_col:
                wineval += f".transform(**{function})"
            else:
                wineval += f".{function.pop('func')}(**{function})"
        else:
            parameters = winjson.get("windowing").get("parameters")
            if parameters:
                if parameters.get('window'):
                    parameters['window'] = int(parameters.get('window'))
                if parameters.get('min_periods'):
                    parameters['min_periods'] = int(parameters.get('min_periods'))
                else:
                    parameters['min_periods'] = 0
            wineval += f".{win_type}(**parameters)"
            wineval += f".{function.pop('func')}(**function)"
            if groupby_col:
                wineval += ".reset_index(0,drop=True)"
        return wineval

    def get_data(self):
        return self.df

    def get_json_data(self):
        return json.loads(DataFrame.to_json(self.df))

    def get_columns(self, flow, node_id, clause_idx=None, parent=False):
        # The below function call gets the data of the current node
        data_list = self.run_data_item(flow, node_id, clause_idx, parent)
        nodeColumns = []

        for data in data_list:
            func = data.pop('func')
            if data.get('copy'):
                data.pop('copy')
            df=func(flow, **data)
            columns = df.convert_dtypes().dtypes
            columnNames = []
            for name,d_type in columns.items():
                columnNames.append({"name": name, "type": str(d_type)})
            try:
                tablename = data['node_id'] if clause_idx == 0 else node_id
            except:
                tablename = node_id
            nodeColumns.append({"tableName": tablename, "columns": columnNames})
        return nodeColumns

    @classmethod
    def column_uniquify(self, columns):
        new_columns = []
        for item in columns:
            counter = 0
            newitem = str(item)
            while newitem in new_columns:
                counter += 1
                newitem = "{}_{}".format(item, counter)
            new_columns.append(newitem)
        return new_columns

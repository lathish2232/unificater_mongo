var db = connect('127.0.0.1:27017/unificaterFlowsDEV');
db.outpytTypes.deleteMany({});
db.outpytTypes.insertMany([
  {
    "outputTypes": [
      {
        "id": "connTypeId_1",
        "type": "csv",
        "displayName": "CSV",
        "functionName": "to_csv",
        "outputParameters": [
          {
            "id": "fieldId_1",
            "fieldName": "path_or_buf",
            "displayName": "file Path",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": true,
            "help": "File path or object, if None is provided the result is returned as"
          },
          {
            "id": "fieldId_2",
            "fieldName": "sep",
            "displayName": "separator",
            "userValue": null,
            "defaultValue": ",",
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "String of length 1. Field delimiter for the output file."
          },
          {
            "id": "fieldId_3",
            "fieldName": "na_rep",
            "displayName": "na_rep",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Missing data representation."
          },
          {
            "id": "fieldId_4",
            "fieldName": "float_format",
            "displayName": "float_format",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Format string for floating point numbers."
          },
          {
            "id": "fieldId_5",
            "fieldName": "columns",
            "displayName": "columns",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": " sequence, optional",
            "type": "input",
            "isRequired": false,
            "help": "Columns to write."
          },
          {
            "id": "fieldId_6",
            "fieldName": "header",
            "displayName": "header",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Write out the column names. If a list of strings is given it is"
          },
          {
            "id": "fieldId_7",
            "fieldName": "index",
            "displayName": "index",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "Boolean",
            "type": "input",
            "isRequired": false,
            "help": "Write row names (index)."
          },
          {
            "id": "fieldId_8",
            "fieldName": "index_label",
            "displayName": "index_label",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Column label for index column(s) if desired. If None is given, and"
          },
          {
            "id": "fieldId_9",
            "fieldName": "mode",
            "displayName": "mode",
            "userValue": null,
            "defaultValue": "w",
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Python write mode, default value is  'w'"
          },
          {
            "id": "fieldId_10",
            "fieldName": "encoding",
            "displayName": "encoding",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "A string representing the encoding to use in the output file,"
          },
          {
            "id": "fieldId_11",
            "fieldName": "compression",
            "displayName": "compression",
            "userValue": null,
            "defaultValue": "infer",
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "If str, represents compression mode. If dict, value at 'method' is"
          },
          {
            "id": "fieldId_12",
            "fieldName": "quoting",
            "displayName": "quoting",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": " optional constant from csv module",
            "type": "input",
            "isRequired": false,
            "help": "Defaults to csv.QUOTE_MINIMAL. If you have set a `float_format`"
          },
          {
            "id": "fieldId_13",
            "fieldName": "quotechar",
            "displayName": "quotechar",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "String of length 1. Character used to quote fields."
          },
          {
            "id": "fieldId_14",
            "fieldName": "line_terminator",
            "displayName": "line_terminator",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "The newline character or character sequence to use in the output"
          },
          {
            "id": "fieldId_15",
            "fieldName": "chunksize",
            "displayName": "chunksize",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "Integer",
            "type": "input",
            "isRequired": false,
            "help": "Rows to write at a time."
          },
          {
            "id": "fieldId_16",
            "fieldName": "date_format",
            "displayName": "date_format",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Format string for datetime objects."
          },
          {
            "id": "fieldId_17",
            "fieldName": "doublequote",
            "displayName": "doublequote",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "Boolean",
            "type": "input",
            "isRequired": false,
            "help": "Control quoting of `quotechar` inside a field."
          },
          {
            "id": "fieldId_18",
            "fieldName": "escapechar",
            "displayName": "escapechar",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "String of length 1. Character used to escape `sep` and `quotechar`"
          },
          {
            "id": "fieldId_19",
            "fieldName": "decimal",
            "displayName": "decimal",
            "userValue": null,
            "defaultValue": ".",
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Character recognized as decimal separator. E.g. use ',' for"
          },
          {
            "id": "fieldId_20",
            "fieldName": "errors",
            "displayName": "errors",
            "userValue": null,
            "defaultValue": "strict",
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Specifies how encoding and decoding errors are to be handled."
          }
        ]
      },
      {
        "id": "connTypeId_2",
        "type": "excel",
        "displayName": "Excel",
        "functionName": "to_excel",
        "outputParameters": [
          {
            "id": "fieldId_1",
            "fieldName": "excel_writer",
            "displayName": "excel_writer",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": true,
            "help": "File path or existing ExcelWriter."
          },
          {
            "id": "fieldId_2",
            "fieldName": "sheet_name",
            "displayName": "sheet_name",
            "userValue": null,
            "defaultValue": "Sheet1",
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Name of sheet which will contain DataFrame."
          },
          {
            "id": "fieldId_3",
            "fieldName": "na_rep",
            "displayName": "na_rep",
            "userValue": null,
            "defaultValue": "",
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Missing data representation."
          },
          {
            "id": "fieldId_4",
            "fieldName": "float_format",
            "displayName": "float_format",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Format string for floating point numbers. For example"
          },
          {
            "id": "fieldId_5",
            "fieldName": "columns",
            "displayName": "columns",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Columns to write."
          },
          {
            "id": "fieldId_6",
            "fieldName": "header",
            "displayName": "header",
            "userValue": null,
            "defaultValue": true,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Write out the column names. If a list of string is given it is"
          },
          {
            "id": "fieldId_7",
            "fieldName": "index",
            "displayName": "index",
            "userValue": null,
            "defaultValue": true,
            "parameterDataType": "Boolean",
            "type": "input",
            "isRequired": false,
            "help": "Write row names (index)."
          },
          {
            "id": "fieldId_8",
            "fieldName": "index_label",
            "displayName": "index_label",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Column label for index column(s) if desired. If not specified, and"
          },
          {
            "id": "fieldId_9",
            "fieldName": "startrow",
            "displayName": "startrow",
            "userValue": null,
            "defaultValue": 0,
            "parameterDataType": "Integer",
            "type": "input",
            "isRequired": false,
            "help": "Upper left cell row to dump data frame."
          },
          {
            "id": "fieldId_10",
            "fieldName": "startcol",
            "displayName": "startcol",
            "userValue": null,
            "defaultValue": 0,
            "parameterDataType": "Integer",
            "type": "input",
            "isRequired": false,
            "help": "Upper left cell column to dump data frame."
          },
          {
            "id": "fieldId_11",
            "fieldName": "engine",
            "displayName": "engine",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Write engine to use, 'openpyxl' or 'xlsxwriter'. You can also set this"
          },
          {
            "id": "fieldId_12",
            "fieldName": "merge_cells",
            "displayName": "merge_cells",
            "userValue": null,
            "defaultValue": true,
            "parameterDataType": "Boolean",
            "type": "input",
            "isRequired": false,
            "help": "Write MultiIndex and Hierarchical Rows as merged cells."
          },
          {
            "id": "fieldId_13",
            "fieldName": "encoding",
            "displayName": "encoding",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Encoding of the resulting excel file. Only necessary for xlwt,"
          },
          {
            "id": "fieldId_14",
            "fieldName": "inf_rep",
            "displayName": "inf_rep",
            "userValue": null,
            "defaultValue": "inf",
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Representation for infinity (there is no native representation for"
          },
          {
            "id": "fieldId_15",
            "fieldName": "verbose",
            "displayName": "verbose",
            "userValue": null,
            "defaultValue": true,
            "parameterDataType": "Boolean",
            "type": "input",
            "isRequired": false,
            "help": "Display more information in the error logs."
          },
          {
            "id": "fieldId_16",
            "fieldName": "freeze_panes",
            "displayName": "freeze_panes",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "Integer",
            "type": "input",
            "isRequired": false,
            "help": "Specifies the one-based bottommost row and rightmost column that"
          }
        ]
      },
      {
        "id": "connTypeId_3",
        "type": "database",
        "displayName": "Database",
        "functionName": "to_sql",
        "outputParameters": [
          {
            "id": "fieldId_1",
            "fieldName": "name",
            "displayName": "Table Name",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": true,
            "help": "Name of SQL table."
          },
          {
            "id": "fieldId_2",
            "fieldName": "con",
            "displayName": "connections",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": " sqlalchemy.engine.(Engine or Connection) or sqlite3.Connection",
            "type": "input",
            "isRequired": true,
            "help": "Using SQLAlchemy makes it possible to use any DB supported by that"
          },
          {
            "id": "fieldId_3",
            "fieldName": "schema",
            "displayName": "schema",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": true,
            "help": "Specify the schema (if database flavor supports this). If None, use"
          },
          {
            "id": "fieldId_4",
            "fieldName": "if_exists",
            "displayName": "if_exists",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": " {'fail', 'replace', 'append'}, default 'fail'",
            "type": "input",
            "isRequired": true,
            "help": "How to behave if the table already exists."
          },
          {
            "id": "fieldId_5",
            "fieldName": "index",
            "displayName": "index",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "Boolean",
            "type": "input",
            "isRequired": false,
            "help": "Write DataFrame index as a column. Uses `index_label` as the column"
          },
          {
            "id": "fieldId_6",
            "fieldName": "index_label",
            "displayName": "index_label",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": false,
            "help": "Column label for index column(s). If None is given (default) and"
          },
          {
            "id": "fieldId_7",
            "fieldName": "chunksize",
            "displayName": "chunksize",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "Integer",
            "type": "input",
            "isRequired": false,
            "help": "Specify the number of rows in each batch to be written at a time."
          },
          {
            "id": "fieldId_8",
            "fieldName": "dtype",
            "displayName": "dtype",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": "Dictionary",
            "type": "input",
            "isRequired": false,
            "help": "Specifying the datatype for columns. If a dictionary is used, the"
          },
          {
            "id": "fieldId_9",
            "fieldName": "method",
            "displayName": "method",
            "userValue": null,
            "defaultValue": null,
            "parameterDataType": " {None, 'multi', callable}, optional",
            "type": "input",
            "isRequired": false,
            "help": null
          }
        ]
      }
    ]
  }
]);

outpytType = db.outpytTypes.find();

while (outpytType.hasNext()) {
   printjson(outpytType.next());
}
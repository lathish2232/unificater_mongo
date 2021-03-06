var db = connect('127.0.0.1:27017/unificaterFlowsDEV');
db.dataSource.deleteMany({});
db.dataSource.insertMany([{
  "connectionJson": {
    "connectionTypes": [
      {
        "id": "connTypeId_1",
        "type": "file",
        "displayName": "Files",
        "connections": [
          {
            "id": "CSV",
            "displayName": "csv",
            "functionName": "read_csv",
            "isFwf": false,
            "returnType": "DataFrame or TextParser",
            "connectionParameters": [
              {
                "id": "fieldId_1",
                "fieldName": "filepath_or_buffer",
                "displayName": "File Path",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "parameterDefaultValue": null,
                "help": "Any valid string path is acceptable. The string could be a URL. Valid"
              },
              {
                "id": "fieldId_2",
                "fieldName": "delimiter",
                "displayName": "Delimiter",
                "userValue": null,
                "parameterDataType": "List",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": ",",
                "help": "Delimiter to use. If sep is null, the C engine cannot automatically detect"
              },
              {
                "id": "fieldId_3",
                "fieldName": "header",
                "displayName": "Header",
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "infer",
                "help": "Row number(s) to use as the column names, and the start of the"
              },
              {
                "id": "fieldId_4",
                "fieldName": "names",
                "displayName": "Names",
                "userValue": null,
                "parameterDataType": " if no names",
                "type": "input",
                "isRequired": false,
                "help": "are passed the behavior is identical to ``header=0`` and column"
              },
              {
                "id": "fieldId_5",
                "fieldName": "index_col",
                "displayName": "Index column",
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "help": "Column(s) to use as the row labels of the ``DataFrame``, either given as"
              },
              {
                "id": "fieldId_6",
                "fieldName": "usecols",
                "displayName": "select columns",
                "userValue": null,
                "parameterDataType": "List",
                "type": "input",
                "isRequired": false,
                "help": "Return a subset of the columns. If list-like, all elements must either"
              },
              {
                "id": "fieldId_7",
                "fieldName": "squeeze",
                "displayName": "squeeze",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": "If the parsed data only contains one column then return a Series."
              },
              {
                "id": "fieldId_8",
                "fieldName": "prefix",
                "displayName": "Prefix to Add Columns",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "help": "Prefix to add to column numbers when no header, e.g. 'X' for X0, X1, ..."
              },
              {
                "id": "fieldId_9",
                "fieldName": "mangle_dupe_cols",
                "displayName": "Manage Duplicate Columns",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "true",
                "help": "Duplicate columns will be specified as 'X', 'X.1', ...'X.N', rather than"
              },
              {
                "id": "fieldId_10",
                "fieldName": "dtype",
                "displayName": "Convert DataType of Column",
                "userValue": null,
                "parameterDataType": "Dictionary",
                "type": "input",
                "isRequired": false,
                "help": null
              },
              {
                "id": "fieldId_11",
                "fieldName": "converters",
                "displayName": "converters",
                "userValue": null,
                "parameterDataType": "Dictionary",
                "type": "input",
                "isRequired": false,
                "help": "Dict of functions for converting values in certain columns. Keys can either"
              },
              {
                "id": "fieldId_12",
                "fieldName": "true_values",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "List",
                "type": "input",
                "isRequired": false,
                "help": "Values to consider as true."
              },
              {
                "id": "fieldId_13",
                "fieldName": "false_values",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "List",
                "type": "input",
                "isRequired": false,
                "help": "Values to consider as false."
              },
              {
                "id": "fieldId_14",
                "fieldName": "skipinitialspace",
                "displayName": "Skip spaces after delimiter",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": "Skip spaces after delimiter."
              },
              {
                "id": "fieldId_15",
                "fieldName": "skiprows",
                "displayName": "Number of Lines To Skip on Top",
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "help": "Line numbers to skip (0-indexed) or number of lines to skip (int)"
              },
              {
                "id": "fieldId_16",
                "fieldName": "skipfooter",
                "displayName": "Number of lines at bottom of file to skip",
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "0",
                "help": "Number of lines at bottom of file to skip (Unsupported with engine='c')."
              },
              {
                "id": "fieldId_17",
                "fieldName": "nrows",
                "displayName": "Number of Rows to read in file",
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "help": "Number of rows of file to read. Useful for reading pieces of large files."
              },
              {
                "id": "fieldId_18",
                "fieldName": "na_values",
                "displayName": "Replace Nulls",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "help": "Additional strings to recognize as NA/NaN. If dict passed, specific"
              },
              {
                "id": "fieldId_19",
                "fieldName": "keep_default_na",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "true",
                "help": "Whether or not to include the default NaN values when parsing the data."
              },
              {
                "id": "fieldId_20",
                "fieldName": "na_filter",
                "displayName": "Null Filter",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "true",
                "help": "Detect missing value markers (empty strings and the value of na_values). In data without any NAs, passing na_filter=False can improve the performance of reading a large file."
              },
              {
                "id": "fieldId_21",
                "fieldName": "verbose",
                "displayName": "Count Null Values in NON Numaric columns",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": "Indicate number of NA values placed in non-numeric columns."
              },
              {
                "id": "fieldId_22",
                "fieldName": "skip_blank_lines",
                "displayName": "Skip Blank Lines",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "true",
                "help": "If true, skip over blank lines rather than interpreting as NaN values."
              },
              {
                "id": "fieldId_23",
                "fieldName": "parse_dates",
                "displayName": "parse Date",
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": null
              },
              {
                "id": "fieldId_24",
                "fieldName": "infer_datetime_format",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": "If true and `parse_dates` is enabled, pandas will attempt to infer the"
              },
              {
                "id": "fieldId_25",
                "fieldName": "keep_date_col",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": "If true and `parse_dates` specifies combining multiple columns then"
              },
              {
                "id": "fieldId_26",
                "fieldName": "date_parser",
                "displayName": null,
                "userValue": null,
                "parameterDataType": " function, optional",
                "type": "input",
                "isRequired": false,
                "help": "Function to use for converting a sequence of string columns to an  of"
              },
              {
                "id": "fieldId_27",
                "fieldName": "dayfirst",
                "displayName": "Keep day as first",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": "DD/MM format dates, international and European format."
              },
              {
                "id": "fieldId_28",
                "fieldName": "cache_dates",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "true",
                "help": "If true, use a cache of unique, converted dates to apply the datetime"
              },
              {
                "id": "fieldId_29",
                "fieldName": "iterator",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": "Return TextFileReader object for iteration or getting chunks with"
              },
              {
                "id": "fieldId_30",
                "fieldName": "chunksize",
                "displayName": "Chunk Size",
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "help": "Return TextFileReader object for iteration."
              },
              {
                "id": "fieldId_31",
                "fieldName": "compression",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "['infer', 'gzip', 'bz2', 'zip', 'xz', null]",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "infer",
                "help": "For on-the-fly decompression of on-disk data. If 'infer' and"
              },
              {
                "id": "fieldId_32",
                "fieldName": "thousands",
                "displayName": "Thousands separator for Numaric columns",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "help": "Thousands separator."
              },
              {
                "id": "fieldId_33",
                "fieldName": "decimal",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": ".",
                "help": "Character to recognize as decimal point (e.g. use ',' for European data)."
              },
              {
                "id": "fieldId_34",
                "fieldName": "lineterminator",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "help": "Character to break file into lines. Only valid with C parser."
              },
              {
                "id": "fieldId_35",
                "fieldName": "quotechar",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "''",
                "help": "The character used to denote the start and end of a quoted item. Quoted"
              },
              {
                "id": "fieldId_36",
                "fieldName": "quoting",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "0",
                "help": "Control field quoting behavior per ``csv.QUOTE_*`` constants. Use one of"
              },
              {
                "id": "fieldId_37",
                "fieldName": "doublequote",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "true",
                "help": "When quotechar is specified and quoting is not ``QUOTE_null``, indicate"
              },
              {
                "id": "fieldId_38",
                "fieldName": "escapechar",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "help": "One-character string used to escape other characters."
              },
              {
                "id": "fieldId_39",
                "fieldName": "comment",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "help": "Indicates remainder of line should not be parsed. If found at the beginning"
              },
              {
                "id": "fieldId_40",
                "fieldName": "encoding",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "help": "Encoding to use for UTF when reading/writing (ex. 'utf-8'). `List of Python"
              },
              {
                "id": "fieldId_41",
                "fieldName": "dialect",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "help": "If provided, this parameter will override values (default or not) for the"
              },
              {
                "id": "fieldId_42",
                "fieldName": "error_bad_lines",
                "displayName": "Drop Bad lines",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "true",
                "help": "Lines with too many fields (e.g. a csv line with too many commas) will by default cause an exception to be raised, and no DataFrame will be returned. If False, then these ???bad lines??? will dropped from the DataFrame that is returned."
              },
              {
                "id": "fieldId_43",
                "fieldName": "warn_bad_lines",
                "displayName": "Warn Each Bad line",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "true",
                "help": "If error_bad_lines is false, and warn_bad_lines is true, a warning for each"
              },
              {
                "id": "fieldId_44",
                "fieldName": "delim_whitespace",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": "Specifies whether or not whitespace (e.g. `` '`` or ``'\\t'``) will be"
              },
              {
                "id": "fieldId_45",
                "fieldName": "low_memory",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "true",
                "help": "Internally process the file in chunks, resulting in lower memory use"
              },
              {
                "id": "fieldId_46",
                "fieldName": "memory_map",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "false",
                "help": "If a filepath is provided for `filepath_or_buffer`, map the file object"
              },
              {
                "id": "fieldId_47",
                "fieldName": "float_precision",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "help": "Specifies which converter the C engine should use for floating-point"
              }
            ]
          },
          {
            "id": "FWF",
            "displayName": "Fixed width file",
            "functionName": "read_FWF",
            "isFwf": true,
            "returnType": null,
            "connectionParameters": [
              {
                "id": "fieldId_1",
                "fieldName": "filepath_or_buffer",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "Any valid string path is acceptable. The string could be a URL. Valid"
              },
              {
                "id": "fieldId_2",
                "fieldName": "colspecs",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "infer",
                "help": "A list of tuples giving the extents of the fixed-width"
              },
              {
                "id": "fieldId_3",
                "fieldName": "widths",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "help": "A list of field widths which can be used instead of 'colspecs' if"
              },
              {
                "id": "fieldId_4",
                "fieldName": "infer_nrows",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "100",
                "help": "The number of rows to consider when letting the parser determine the"
              }
            ]
          },
          {
            "id": "excel",
            "displayName": "Excel",
            "functionName": "read_excel",
            "isFwf": false,
            "returnType": "DataFrame or TextParser",
            "connectionParameters": [
              {
                "id": "fieldId_1",
                "fieldName": "io",
                "displayName": "Excel File Path",
                "userValue": null,
                "parameterDataType": [
                  "string",
                  "bytes"
                ],
                "type": "input",
                "isRequired": true,
                "parameterDefaultValue": null,
                "help": "Any valid string path is acceptable. The string could be a URL. Valid URL schemes include http, ftp, s3, and file. For file URLs, a host is expected. A local file could be"
              },
              {
                "id": "fieldId_2",
                "fieldName": "sheet_name",
                "displayName": "Sheet Name",
                "userValue": null,
                "parameterDataType": [
                  "string",
                  "Integer",
                  "List",
                  "None"
                ],
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": 0,
                "help": "Strings are used for sheet names. Integers are used in zero-indexed sheet positions. Lists of strings/Integers are used to request multiple sheets. Specify None to get all sheets."
              },
              {
                "id": "fieldId_3",
                "fieldName": "header",
                "displayName": "Header",
                "userValue": null,
                "parameterDataType": [
                  "Integer",
                  "List of Integers"
                ],
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": 0,
                "help": "Row (0-indexed) to use for the column labels of the parsed DataFrame. If a List of Integers is passed those row positions will be combined into a MultiIndex. Use None if there is no header."
              },
              {
                "id": "fieldId_4",
                "fieldName": "names",
                "displayName": "Names",
                "userValue": null,
                "parameterDataType": "List",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "List of column names to use. If file contains no header row, then you should explicitly pass header=None"
              },
              {
                "id": "fieldId_5",
                "fieldName": "index_col",
                "displayName": "Index column",
                "userValue": null,
                "parameterDataType": [
                  "Integer",
                  "string"
                ],
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Column (0-indexed) to use as the row labels of the DataFrame. Pass None if there is no such column."
              },
              {
                "id": "fieldId_6",
                "fieldName": "usecols",
                "displayName": "select Columns",
                "userValue": null,
                "parameterDataType": [
                  "Integer",
                  "string",
                  "List"
                ],
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "select columns passing column names if required, if none of them passed then select all columns  "
              },
              {
                "id": "fieldId_7",
                "fieldName": "squeeze",
                "displayName": "squeeze",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": false,
                "help": "If the parsed data only contains one column then return a Series."
              },
              {
                "id": "fieldId_8",
                "fieldName": "converters",
                "displayName": "converters",
                "userValue": null,
                "parameterDataType": "Dictionary",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Dict of functions for converting values in certain columns. Keys can either"
              },
              {
                "id": "fieldId_9",
                "fieldName": "true_values",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "List",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Values to consider as true."
              },
              {
                "id": "fieldId_10",
                "fieldName": "false_values",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "List",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Values to consider as false."
              },
              {
                "id": "fieldId_11",
                "fieldName": "skiprows",
                "displayName": "Number of Lines To Skip on Top",
                "userValue": null,
                "parameterDataType": null,
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Line numbers to skip (0-indexed) or number of lines to skip (int)"
              },
              {
                "id": "fieldId_12",
                "fieldName": "nrows",
                "displayName": "Number of Rows to read in file",
                "userValue": null,
                "parameterDataType": null,
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Number of rows of file to read. Useful for reading pieces of large files."
              },
              {
                "id": "fieldId_13",
                "fieldName": "na_values",
                "displayName": "Replace Nulls",
                "userValue": null,
                "parameterDataType": null,
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Additional strings to recognize as NA/NaN. If dict passed, specific"
              },
              {
                "id": "fieldId_14",
                "fieldName": "parse_dates",
                "displayName": null,
                "userValue": null,
                "parameterDataType": null,
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": false,
                "help": null
              },
              {
                "id": "fieldId_15",
                "fieldName": "date_parser",
                "displayName": null,
                "userValue": null,
                "parameterDataType": " function, optional",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Function to use for converting a sequence of string columns to an  of"
              },
              {
                "id": "fieldId_16",
                "fieldName": "thousands",
                "displayName": "Thousands separator for Numaric columns",
                "userValue": null,
                "parameterDataType": null,
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Thousands separator."
              },
              {
                "id": "fieldId_17",
                "fieldName": "comment",
                "displayName": "comment",
                "userValue": null,
                "parameterDataType": null,
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": null
              },
              {
                "id": "fieldId_18",
                "fieldName": "skipfooter",
                "displayName": "Number of lines at bottom of file to skip",
                "userValue": null,
                "parameterDataType": null,
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": 0,
                "help": "Number of lines at bottom of file to skip."
              },
              {
                "id": "fieldId_19",
                "fieldName": "convert_float",
                "displayName": "convert Flot values",
                "userValue": null,
                "parameterDataType": null,
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": true,
                "help": null
              },
              {
                "id": "fieldId_20",
                "fieldName": "mangle_dupe_cols",
                "displayName": "Manage Duplicate Columns",
                "userValue": null,
                "parameterDataType": null,
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": true,
                "help": "Duplicate columns will be specified as 'X', 'X.1', ...'X.N', rather than"
              }
            ]
          },
          {
            "id": "json",
            "displayName": "Json File",
            "functionName": "read_json",
            "isFwf": false,
            "returnType": "Series or DataFrame",
            "connectionParameters": [
              {
                "id": "fieldId_1",
                "fieldName": "path_or_buf",
                "displayName": "Json File Path",
                "userValue": null,
                "parameterDataType": [
                  "string",
                  "bytes"
                ],
                "type": "input",
                "isRequired": true,
                "parameterDefaultValue": null,
                "help": "Any valid string path is acceptable. The string could be a URL. Valid URL schemes include http, ftp, s3, and file. For file URLs, a host is expected. A local file could be"
              },
              {
                "id": "fieldId_2",
                "fieldName": "orient",
                "displayName": "orient",
                "userValue": null,
                "parameterDataType": "string",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": 0,
                "help": " Indication of expected JSON string format. Compatible JSON strings can be produced by to_json() with a corresponding orient value. The set of possible orients is"
              },
              {
                "id": "fieldId_3",
                "fieldName": "typ",
                "displayName": "Object Type",
                "userValue": null,
                "parameterDataType": "string",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "frame",
                "help": "The type of object to recover."
              },
              {
                "id": "fieldId_4",
                "fieldName": "dtype",
                "displayName": "data types",
                "userValue": null,
                "parameterDataType": [
                  "Integer",
                  "string"
                ],
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "If true, infer dtypes; if a dict of column to dtype, then use those; if false, then don???t infer dtypes at all, applies only to the data."
              },
              {
                "id": "fieldId_5",
                "fieldName": "convert_axes",
                "displayName": "convert_axes",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "select columns passing column names if required, if null of them passed then select all columns  "
              },
              {
                "id": "fieldId_6",
                "fieldName": "convert_dates",
                "displayName": "Convert Dates",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": true,
                "help": "If the parsed data only contains one column then return a Series."
              },
              {
                "id": "fieldId_7",
                "fieldName": "keep_default_dates",
                "displayName": "Keep Default Dates",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": true,
                "help": "Dict of functions for converting values in certain columns. Keys can either"
              },
              {
                "id": "fieldId_8",
                "fieldName": "precise_float",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "List",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": false,
                "help": "Set to enable usage of higher precision (strtod) function when decoding string to double values. Default (false) is to use fast but less precise builtin functionality"
              },
              {
                "id": "fieldId_9",
                "fieldName": "date_unit",
                "displayName": "Date Units",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Values to consider as true."
              },
              {
                "id": "fieldId_10",
                "fieldName": "encoding",
                "displayName": "Encoding",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": "utf-8",
                "help": "The encoding to use to decode py3 bytes."
              },
              {
                "id": "fieldId_11",
                "fieldName": "lines",
                "displayName": "Number of Lines To Skip on Top",
                "userValue": null,
                "parameterDataType": "Boolean",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": false,
                "help": "Read the file as a json object per line"
              },
              {
                "id": "fieldId_12",
                "fieldName": "chunksize",
                "displayName": "Number of Rows to read in file",
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Number of rows of file to read. Useful for reading pieces of large files."
              },
              {
                "id": "fieldId_13",
                "fieldName": "compression",
                "displayName": "Replace nulls",
                "userValue": null,
                "parameterDataType": [
                  "infer",
                  "gzip",
                  "bz2",
                  "Zip",
                  "xz"
                ],
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "Additional strings to recognize as NA/NaN. If dict passed, specific"
              },
              {
                "id": "fieldId_14",
                "fieldName": "nrows",
                "displayName": null,
                "userValue": null,
                "parameterDataType": "Integer",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": false,
                "help": "optional"
              }
            ]
          }
        ]
      },
      {
        "id": "connTypeId_2",
        "type": "pattern",
        "displayName": "Pattern",
        "connections": [{
          "id": "patternId_1",
          "name": "csv",
          "displayName": "CSV Files",
          "connectionParameters": [{
            "id": "fieldId_1",
            "fieldName": "instances_name",
            "displayName": "Instances Name",
            "userValue": null,
            "parameterDataType": "String",
            "type": "input",
            "isRequired": true,
            "help": "Any valid string path is acceptable. The string could be a URL. Valid"
          },
          {
            "id": "fieldId_2",
            "fieldName": "filepath_or_buffer",
            "displayName": "Folder path with pattern",
            "userValue": null,
            "parameterDataType": "List",
            "type": "input",
            "isRequired": true,
            "parameterDefaultValue": null,
            "help": "proide folder path with pattern example:-c:/users/admin/data/*.csv or c:/users/admin/data/*.xlsx etc"
          }]

      },
      {
        "id": "patternId_2",
        "name": "text",
        "displayName": "Text Files",
        "connectionParameters": [{
          "id": "fieldId_1",
          "fieldName": "instances_name",
          "displayName": "Instances Name",
          "userValue": null,
          "parameterDataType": "String",
          "type": "input",
          "isRequired": true,
          "help": "Any valid string path is acceptable. The string could be a URL. Valid"
        },
        {
          "id": "fieldId_2",
          "fieldName": "filepath_or_buffer",
          "displayName": "Folder path with pattern",
          "userValue": null,
          "parameterDataType": "List",
          "type": "input",
          "isRequired": true,
          "parameterDefaultValue": null,
          "help": "proide folder path with pattern example:-c:/users/admin/data/*.csv or c:/users/admin/data/*.xlsx etc"
        }]

    }

    ]
      },
      {
        "id": "connTypeId_3",
        "type": "database",
        "displayName": "Database",
        "connections": [
          {
            "id": "dbId_1",
            "name": "postgreSql",
            "displayName": "PostgreSQL",
            "functionName": "read_sql",
            "isFwf": false,
            "returnType": null,
            "connectionParameters": [
              {
                "id": "fieldId_1",
                "fieldName": "instanceName",
                "displayName": "Instance Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "Any valid string is acceptable. The string could be Valid"
              },
              {
                "id": "fieldId_2",
                "fieldName": "hostAddress",
                "displayName": "Host Address",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "host name is required to connect database"
              },
              {
                "id": "fieldId_3",
                "fieldName": "userName",
                "displayName": "User Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "please provide user name"
              },
              {
                "id": "fieldId_4",
                "fieldName": "password",
                "displayName": "Password",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "please provide password"
              },
              {
                "id": "fieldId_5",
                "fieldName": "database",
                "displayName": "Database",
                "userValue": null,
                "parameterDataType": "integer",
                "type": "input",
                "isRequired": true,
                "help": "please provide database name"
              },
              {
                "id": "fieldId_6",
                "fieldName": "portNo",
                "displayName": "Port Number",
                "userValue": null,
                "parameterDataType": "integer",
                "type": "input",
                "isRequired": false,
                "help": "port number should be integer"
              }
            ]
          },
          {
            "id": "dbId_2",
            "name": "MSSQL",
            "displayName": "Microsoft SQL server",
            "functionName": "read_sql",
            "isFwf": false,
            "returnType": null,
            "connectionParameters": [
              {
                "id": "fieldId_1",
                "fieldName": "instanceName",
                "displayName": "Instance Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "Any valid string is acceptable. The string could be Valid"
              },
              {
                "id": "fieldId_2",
                "fieldName": "hostAddress",
                "displayName": "Host Address",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "host name is required to connect database"
              },
              {
                "id": "fieldId_3",
                "fieldName": "database",
                "displayName": "Database Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "Data base should be string"
              },
              {
                "id": "fieldId_4",
                "fieldName": "userName",
                "displayName": "User Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "please provide user name"
              },
              {
                "id": "fieldId_5",
                "fieldName": "password",
                "displayName": "Password",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "please provide password"
              },
              {
                "id": "fieldId_6",
                "fieldName": "portNo",
                "displayName": "Port Number",
                "userValue": null,
                "parameterDataType": "integer",
                "type": "input",
                "isRequired": false,
                "help": "port number should be integer"
              }
            ]
          },
          {
            "id": "dbId_3",
            "name": "mySql",
            "displayName": "MySQL",
            "functionName": "read_sql",
            "isFwf": false,
            "returnType": null,
            "connectionParameters": [
              {
                "id": "fieldId_1",
                "fieldName": "instanceName",
                "displayName": "Instance Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "Any valid string is acceptable. The string could be Valid"
              },
              {
                "id": "fieldId_2",
                "fieldName": "hostAddress",
                "displayName": "Host Address",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "host name is required to connect database"
              },
              {
                "id": "fieldId_3",
                "fieldName": "userName",
                "displayName": "User Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "please provide user name"
              },
              {
                "id": "fieldId_4",
                "fieldName": "password",
                "displayName": "Password",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "please provide password"
              },
              {
                "id": "fieldId_5",
                "fieldName": "portNo",
                "displayName": "Port Number",
                "userValue": null,
                "parameterDataType": "integer",
                "type": "input",
                "isRequired": false,
                "help": "port number should be integer"
              },
              {
                "id": "fieldId_6",
                "fieldName": "database",
                "displayName": "Database Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "Data base should be string"
              }
            ]
          },
          {
            "id": "dbId_4",
            "name": "oracle",
            "displayName": "Oracle",
            "functionName": "read_sql",
            "isFwf": false,
            "returnType": null,
            "connectionParameters": [
              {
                "id": "fieldId_1",
                "fieldName": "instanceName",
                "displayName": "Instance Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "Any valid string is acceptable. The string could be Valid"
              },
              {
                "id": "fieldId_2",
                "fieldName": "hostAddress",
                "displayName": "Host Address",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "host name is required to connect database"
              },
              {
                "id": "fieldId_3",
                "fieldName": "userName",
                "displayName": "User Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "please provide user name"
              },
              {
                "id": "fieldId_4",
                "fieldName": "password",
                "displayName": "Password",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "please provide password"
              },
              {
                "id": "fieldId_5",
                "fieldName": "portNo",
                "displayName": "Port Number",
                "userValue": null,
                "parameterDataType": "integer",
                "type": "input",
                "isRequired": false,
                "help": "port number should be integer"
              },
              {
                "id": "fieldId_6",
                "fieldName": "database",
                "displayName": "Database Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "Data base should be string"
              }
            ]
          }
        ]
      },
      {
        "id": "connTypeId_4",
        "type": "restapi",
        "displayName": "Rest Api",
        "connections": [
          {
            "id": "api",
            "displayName": "API",
            "isFwf": false,
            "returnType": null,
            "connectionParameters": [
              {
                "id": "fieldId_1",
                "fieldName": "instances_name",
                "displayName": "Instances Name",
                "userValue": null,
                "parameterDataType": "String",
                "type": "input",
                "isRequired": true,
                "help": "Any valid string path is acceptable. The string could be a URL. Valid"
              },
              {
                "id": "fieldId_2",
                "fieldName": "url",
                "displayName": "URL or API End Point",
                "userValue": null,
                "parameterDataType": "List",
                "type": "input",
                "isRequired": false,
                "parameterDefaultValue": null,
                "help": "url is Required"
              }
            ]
          }
        ]
      }
    ]
  }
}]);

dataSource = db.dataSource.find();

while (dataSource.hasNext()) {
   printjson(dataSource.next());
}
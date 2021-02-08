import numpy as np
import pandas as pd
import sqlite3

def smmry(df):
    display(df.info(), df.memory_usage(deep=True), df.head())

def csnap(df, fn=lambda x: x.shape, msg=None):
    """ Custom Help function to print things in method chaining.
        Returns back the df to further use in chaining.
    """
    if msg:
        print(msg)
    display(fn(df))
    return df

def setcols(df, fn=lambda x: x.columns.map('_'.join), cols=None):
    """Sets the column of the data frame to the passed column list.
    """
    if cols:
        df.columns = cols
    else:
        df.columns = fn(df)
    return df

def cfilter(df, fn, axis="rows"):
    """ Custom Filters based on a condition and returns the df.
        function - a lambda function that returns a binary vector
        thats similar in shape to the dataframe
        axis = rows or columns to be filtered.
        A single level indexing
    """
    if axis == "rows":
        return df[fn(df)]
    elif axis == "columns":
        return df.iloc[:, fn(df)]

def fndf(df, fn, cols):
    df[cols] = fn(df[cols])
    return df

def tonumeric(df, columns):
    df[columns] = df[columns].apply(pd.to_numeric)
    return df

def tocategorical(df, columns):
    df[columns] = df[columns].astype('category')
    return df

def todate(df, columns, frmt=None):
    df[columns] = df[columns].astype(str)
    df[columns] = pd.to_datetime(df[columns], format=frmt)
    return df

def dfToSql(dbpath, table, df, write='replace'):
    con = sqlite3.connect(dbpath)
    df.to_sql(table, con, if_exists=write, index=False)
    print(table + ' is compleded')
    con.close()

def dfFromSql(dbpath, query, params=None):
    con = sqlite3.connect(dbpath)
    df = pd.read_sql(query, con, params=params).reset_index(drop=True)
    con.close()
    return df

def dfFromSqlAll(dbpath):
    "read table names from sql"
    con = sqlite3.connect(dbpath)
    dftable = pd.read_sql("SELECT * FROM sqlite_master", con)
    tablenames = dftable['tbl_name']

    df = pd.DataFrame()
    for index, value in tablenames.items():
        query = "SELECT * FROM " + value
        # print(query)
        temp = pd.read_sql(query, con)
        df = pd.concat([df, temp], sort=False)
    df.reset_index(drop=True)
    con.close()

    return df
import pandas as pd
import sqlite3
from tkinter import messagebox
import re
from Database.CommonSqliteActions import CommonSqliteActions

def fidelityHoldingsImport(csv_file_location):
    sql = CommonSqliteActions()

    try:
        sql.cursor.execute("DELETE FROM fidelity_portfolio")

        panda_store = pd.read_csv(csv_file_location, encoding="utf-8-sig").fillna(0)

        for index, row in panda_store.iterrows():
            if(row['Symbol'] != 0):    
                if re.search("[*\d\s]", row['Symbol']) is None:
                    total_return = row['Total Gain/Loss Dollar'].translate({ord(i): None for i in "$+,)"}).replace('(', '-')
                    equity = row['Cost Basis'].translate({ord(i): None for i in "$,"})
                    total_return_percent = row['Total Gain/Loss Percent'].translate({ord(i): None for i in "%+"})
                    allocation = row['Percent Of Account'].replace('%', '')

                    insert_statement = "INSERT INTO fidelity_portfolio (ticker, name, shares, return, equity, percent_gain, percent_allocation) VALUES (\"{}\", \"{}\", {}, {}, {}, {}, {})".format(row['Symbol'], row['Description'], row['Quantity'], total_return, equity, total_return_percent, allocation)
                    sql.cursor.execute(insert_statement)
        
        sql.closeDb()

        messagebox.showinfo(title="Success", message="Table successfully updated.")

    except sqlite3.OperationalError as error:
        messagebox.showerror(title="Operational error", message=error.args)
    except sqlite3.Error as error:
        messagebox.showerror(title="Database error", message=error.args)
    except TypeError as error:
        messagebox.showerror(title="Type error", message=error.args)
    except KeyError as error:
        messagebox.showerror(title="Mismatching key", message = "The key can not be found in the file; check you are uploading the correct file or check format. Key:" + str(error.args))
    except ValueError:
        messagebox.showerror(title="No File Found", message="Invalid file path or no file selected")

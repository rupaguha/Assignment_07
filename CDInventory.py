#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with text file operations and error handling.
# Change Log: (Who, When, What)
# Rupa Guha, 2020-Aug-23, Created File from last week's homework assignment
# Rupa Guha, 2020-Aug-25, Modified - implemented suggested changes and corrected errors
# Rupa Guha, 2020-Aug-25, Modified - added error handling
# Rupa Guha, 2020-Aug-25, Modified - added binary store read/write code
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #

class DataProcessor:
    # TODone add functions for processing here
    @staticmethod
    def input_data_process(intID, cdTitle, cdArtist, lstTbl):
        """Function to add user input data to table

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            The ID, Title and Artist newly input by the user

        Returns:
            None.
        """
        dicRow = {'ID': intID, 'Title': cdTitle, 'Artist': cdArtist}
        lstTbl.append(dicRow)

    @staticmethod
    def delete_row(rowId, lstTbl):
        """Function to delete row from the inventory

        Args:
            The ID of the row intended to be deleted

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == rowId:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        
        # catching errors like empty file or file not found
        try:
            objFile = open(file_name, 'rb')
            row_line = []
            
            data = pickle.load(objFile)
            
            lstData = data.strip().split('\n')
            
            for item in lstData:
                row_line = item.strip().split(',')
                dicRow = {'ID': int(row_line[0]), 'Title': row_line[1], 'Artist': row_line[2]}
                table.append(dicRow)
                
            objFile.close()
            
        except FileNotFoundError as e:
            print("It looks like the file does not exist.")
            print("Error info: ")
            print(type(e),e, sep="\n")
            
        except ValueError as e:
            print("It looks like the file is empty.")
            print("Error info: ")
            print(type(e),e, sep="\n")
        
            
    def save_file(file_name, table):
        """Function to save the text file

        Writes the data from a 2D table (list of dicts) into a long string and saved into a text file.

        Args:
            file_name (string): name of file used to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        objFile = open(file_name, 'wb')
        new_line = ""
        
        for row in table:
            print(row)
            for item in row.values():
                new_line = new_line + str(item) + ","
            new_line = new_line[:-1] + "\n"

        pickle.dump(new_line, objFile)  
        objFile.close()
        print("Data saved!")


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    # TODone add I/O functions as needed
    @staticmethod
    def ask_user_data():
        """Asks for user data
        
        Args: None
        Returns: The ID, the CD Title and the Artist of the title
        """
        
        # catching errors like entering non-numeric entries
        try:
            ID = int(input('Enter ID: ').strip())
            Title = input('What is the CD\'s title? ').strip()
            Artist = input('What is the Artist\'s name? ').strip()
            return ID, Title, Artist
        except ValueError as e:
            print("Only numbers allowed for ID")
            print("Error info: ")
            print(type(e),e, sep="\n")
            

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        
        # catching error when erroneous data was not passed from IO.ask_user_data()
        try:
            # 3.3.1 Ask user for new ID, CD Title and Artist
            # TODone move IO code into function
            intID, strTitle, stArtist = IO.ask_user_data()
        
        except TypeError as e:
            print("Error in data entry.")
            print("Error info: ")
            print(type(e),e, sep="\n")
            continue
                       
        # 3.3.2 Add item to the table
        # TODone move processing code into function
        DataProcessor.input_data_process(intID, strTitle, stArtist, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        
        # catching error when non-numeric data is entered by user
        try:
            # 3.5.1.2 ask user which ID to remove
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD
            # TODone move processing code into function
            DataProcessor.delete_row(intIDDel, lstTbl)
        except ValueError as e:
            print("Only numbers are allowed!")
            print("Error info: ")
            print(type(e),e, sep="\n")
            continue
            
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            # TODone move processing code into function
            FileProcessor.save_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')





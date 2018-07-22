#Author : Junho, Manggny
import pymysql
import datetime
import sys, os

class MySQL_DATA:
    def __init__(self):
        print("\n")
        self.cur = 0
        self.conn = 0
        self.DataBase_list = []
        self.database_num = 0
        self.Table_list = []
        self.table_num = 0

    def login(self,ID,passwd,IP):
        try:
            self.conn = pymysql.connect(user=ID,passwd=passwd,host=IP,charset='utf8')
            self.cur = self.conn.cursor()
            return 1
        except:
            return 0
               

    def show_databases(self):
        self.cur.execute("show databases;")
        flag = 0
        self.DataBase_list=[] 
        for row in self.cur.fetchall():
#            print(row)
            print(flag, ":",(''.join(row)))
            self.DataBase_list.append((''.join(row)))
            flag += 1
    def select_databases(self):
        #print(self.DataBase_list)
        self.database_num = int(input("[TYPE NUM] Please enter the number of Database :  "))
        print("--The database ***",self.DataBase_list[self.database_num], "*** is selected--")
        print("\n")
        self.cur.execute("use " + self.DataBase_list[self.database_num]+";")

    def show_tables(self):
        self.cur.execute("show tables;")
        flag = 0
        self.Table_list=[]
        for row in self.cur.fetchall():
            print("   ",flag, ":",(''.join(row)))
            self.Table_list.append((''.join(row)))
            flag += 1
    def select_table(self):
        self.table_num = int(input("    [TYPE NUM] Please enter the number of Table :  "))
        print("    --The table ***",self.Table_list[self.table_num], "*** is selected--")
        self.cur.execute("DESC "+self.Table_list[self.table_num] +";")
        for row in self.cur.fetchall():
#            print(''.join(row),end=' ')
            print(row)
        print("\n")
        

    def MySQL_command(self):
        print("MySQL interfaced command line... exit to leave",end='')
        while True:
            print()
            command = input("[TYPE SQL COMMAND] MySQL command : ")
            if command == 'exit':
                break
            try:
                self.cur.execute(command)
            except:
                print("invalid command...")
                continue
            for row in self.cur.fetchall():
#                print(''.join(row))
                print(row)

    def MySQL_Save_Table_to_Text_interface(self):
        print("\n")
        while True:
            print("** This is Save DATA from SQL SERVER to local text file interface **")
            print("** 'cli' to specify the data you want **")
            print("** 'wri' to directly write the text **")
            print("** 'exit' to quit writing process **\n")
            command = input("[1][Choose] Choose one from 'cli', 'wri', 'exit' : ")
            if "cli" in command.lower() :
                self.MySQL_command()
            elif "wri" in command.lower() :
                pass
            elif "exit" in command.lower() :
                print("bye")
                break
            else:
                print("Not correctly input command, to MySQL command line mode, anyway.." )
                self.MySQL_command()
            print("** Now select DB for saving **")
            self.show_databases()
            self.select_databases()
            self.show_tables()
        
            to_first = 0
            while True:
                print()
                to_break = 0
                while True:
                    DESC_table = input(" [2][Choose] Choose 'sel':SELECT, 'desc':DESC, 'exit':exit: ")
                    if "sel" in DESC_table.lower():
                        break
                    elif 'exit' in DESC_table.lower():
                        to_break = 1
                        break
                    else:
                        self.show_tables()
                        self.select_table()
                if(to_break==1):
                    break
                save_text = input("[Data File Name] Targeting output text file.. ex) test.txt :   ")
                while True:
                    save_command = input(" [1][Code Typing select] -*- The SAVING Command : SELECT * FROM ... -*- ('re'/'exit'): ")
                    if "re" == save_command.lower() :
                        to_first = 1
                        break
                    if "exit" == save_command.lower() :
                        to_first = 2
                        break
                    try:
                        self.cur.execute(save_command)
                        Write_list = []
                        for row in self.cur.fetchall():
                            #print(row)
                            temp_list = []
                            for data in row:
                                if type(data) is datetime.date:
                                    data = data.strftime("%Y-%m-%d-%H")
                                temp_list.append(data)
                            Write_list.append(temp_list)
                        #print(Write_list)
                        self.Write_row_list_text(RawList=Write_list, output_text=save_text)
                        break
                    except:
                        print("invalid command... please re-type")

                if(to_first==1):
                    break
                if(to_first==2):
                    break

            if(to_first==1):
                continue
            if(to_first==2):
                print("bye")
                break

    def Write_row_list_text(self,RawList,output_text):
        Of = open(output_text, "w+")
        print("1")
        for i in range(len(RawList)):
            for j in range(len(RawList[i])):
                Of.write("%s" %RawList[i][j])
                if(j != len(RawList[i])-1):
                    Of.write(" ")
                if(j == len(RawList[i])-1):
                    Of.write("\n")
        print("Successfully written selected data into -*-",output_text,"-*- !!")
        Of.close()


def main():
    ID = 'root'; passwd='pyku2018'; IP='154.8.160.186'
    pyku_mysql = MySQL_DATA() 
    status = pyku_mysql.login(ID,passwd,IP)
    if(status==0): 
        print("Server is not responding...")
        return 
    elif(status==1):
        print("--Reached to PYKU Server--\n")    
    #pyku_mysql.MySQL_command()
    pyku_mysql.MySQL_Save_Table_to_Text_interface()

 


if __name__=="__main__":
    main()


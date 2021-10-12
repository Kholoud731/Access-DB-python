## task 1 

import psycopg2


### part used to create the table 

# con = psycopg2.connect(database="postgres", user="postgres", password="Cheetos@75", host="127.0.0.1", port="5432")
# t = con.cursor()
# t.execute('''CREATE TABLE EMPLOYEE(
#    id serial, 
#    fname varCHAR(20) NOT NULL,
#    lname varCHAR(20),
#    AGE INT,
#    depa varCHAR(20),
#    salary integer
# )''')
# con.commit()
# con.close()


### to make sure that the table is empty 

con = psycopg2.connect(database="postgres", user="postgres", password="Cheetos@75", host="127.0.0.1", port="5432")
t = con.cursor()
t.execute('truncate table employee')
con.commit()
con.close()


## connection class

class Conn:


    ## connection methods
    @classmethod 
    def openCon(cls):
        Conn.con = psycopg2.connect(database="postgres", user="postgres", password="Cheetos@75", host="127.0.0.1", port="5432")
        return Conn.con

    @classmethod
    def insertCon(cls, id, fname, lname, age, depa, salary):
        cursor = cls.con.cursor()
        postgres_insert_query = """ INSERT INTO employee (id, fname, lname, age, depa, salary) VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (id, fname, lname, age, depa, salary)
        cursor.execute(postgres_insert_query, record_to_insert)


    @classmethod
    def updateCon(cls, d, id):
        cursor = cls.con.cursor()
        postgres_update_query = """ update employee set depa = %s where id = %s """
        record_to_update = (d, id)
        cursor.execute(postgres_update_query, record_to_update)

    @classmethod
    def deleteCon(cls, id):
        cursor = cls.con.cursor()
        postgres_delete_query = """ delete from employee where id = %s """
        record_to_delete = ([id])
        cursor.execute(postgres_delete_query, record_to_delete)

    @classmethod
    def selectCon(cls,id):
        cursor = cls.con.cursor()
        postgres_select_query = """ select * from employee where id = %s """
        record_to_select = ([id])
        cursor.execute(postgres_select_query,record_to_select)
        return cursor.fetchall() 

    @classmethod
    def commitCon(cls):
        return  cls.con.commit() 

    @classmethod
    def closeCon(cls):
        return  cls.con.close()  




## employee class
class Employee:

    ind = 0
    employee_list = []
    def __init__(self, fname, lname, age, depa, salary):
        
        self.__fname = fname
        self.__lname = lname
        self.__age = age
        self.__depa = depa
        self.__salary = salary
        Employee.ind += 1 
        self.inde = Employee.ind
        empList = [self.inde, self.__fname, self.__lname, self.__age, self.__depa, self.__salary]
        Employee.employee_list.append(empList)
        Conn.openCon()
        Conn.insertCon(*empList)
        Conn.commitCon()
        Conn.closeCon()
        

    @classmethod
    def transfer(cls,d,id):
        Conn.openCon()
        Conn.updateCon(d, id)
        Conn.commitCon()
        Conn.closeCon()
        Employee.employee_list [id - 1][4]= d

    @classmethod    
    def fire(cls, id):
        Employee.employee_list.remove(Employee.employee_list[id - 1])
        Conn.openCon()
        Conn.deleteCon(id)
        Conn.commitCon()
        Conn.closeCon()      

    @classmethod
    def show(cls,id):
        Conn.openCon()
        show = Conn.selectCon(id)
        Conn.commitCon()
        Conn.closeCon() 
        return list(show[0])

    @classmethod
    def list_employees(cls): 
        for emp in Employee.employee_list:
            print(emp)


    # ## connection methods
    # @classmethod 
    # def openCon(cls):
    #     return psycopg2.connect(database="postgres", user="postgres", password="Cheetos@75", host="127.0.0.1", port="5432")

    # @classmethod
    # def insertCon(cls, id, fname, lname, age, depa, salary):
    #     cursor = cls.con.cursor()
    #     postgres_insert_query = """ INSERT INTO employee (id, fname, lname, age, depa, salary) VALUES (%s,%s,%s,%s,%s,%s)"""
    #     record_to_insert = (id, fname, lname, age, depa, salary)
    #     cursor.execute(postgres_insert_query, record_to_insert)


    # @classmethod
    # def updateCon(cls, d, id):
    #     cursor = cls.con.cursor()
    #     postgres_update_query = """ update employee set depa = %s where id = %s """
    #     record_to_update = (d, id)
    #     cursor.execute(postgres_update_query, record_to_update)

    # @classmethod
    # def deleteCon(cls, id):
    #     cursor = cls.con.cursor()
    #     postgres_delete_query = """ delete from employee where id = %s """
    #     record_to_delete = ([id])
    #     cursor.execute(postgres_delete_query, record_to_delete)

    # @classmethod
    # def selectCon(cls,id):
    #     cursor = cls.con.cursor()
    #     postgres_select_query = """ select * from employee where id = %s """
    #     record_to_select = ([id])
    #     cursor.execute(postgres_select_query,record_to_select)
    #     return cursor.fetchall() 

    # @classmethod
    # def commitCon(cls):
    #     return  cls.con.commit() 

    # @classmethod
    # def closeCon(cls):
    #     return  cls.con.close()   


class Manager(Employee):
    def __init__(self, fname, lname, age, depa, salary, managed_department):
        super().__init__(fname, lname, age, depa, salary)
        self.managed_department = managed_department  

    @classmethod
    def show(cls, id):
        manger = super().show(id)
        manger[-1] = "confidential"
        return manger
           
# ## test cases 
# emp1 = Employee('kholoud', 'talaat', 27, 'a', 50000)
# emp2 = Employee('kholoud', 'talaat', 27, 'b', 50000)
# emp3 = Employee('kholoud', 'talaat', 27, 'b', 50000)
# Employee.transfer('1', 1)
# Employee.transfer('2', 2)
# Employee.transfer('3', 3)
# Employee.fire(2)
# print(Employee.show(3))
# man1 = Manager('kholoud','talaat', 25, 'a', 70000,'2')
# print(Manager.show(4))


## app to insert the employees 

## menu for the operations 

print("""
Hello, Please find the following keywords to use the app:
""")

## input to ask for operation 

op = ""
emp_id_list = []
man_id_list = []
while op != "q":
    op = input('''
    a: to add new user
    m: to specify it's a manager 
    e: for normal employees 
    s: to show the emplyee you entered 
    l: to list all the employess 
    f: to delete the employee using the id 
    t: to change the department for one od the users 
    q: to quit the process 
    How can we help??: ''')

    if op == 'a':
        po = input('Employee e/ Manager m: ')
        if po == 'e':
            fname = input('first name: ')
            lname = input('last name: ')
            age = input('age : ')
            dep = input('department: ')
            salary = input('salary: ')
            e = Employee(fname,lname, age, dep, salary)
            emp_id_list.append(e.inde)
         
        if po == 'm':
            fname = input('first name: ')
            lname = input('last name: ')
            age = input('age : ')
            dep = input('department: ')
            salary = input('salary: ')
            man_dep = input('department to manage: ')
            m = Manager(fname,lname, age, dep, salary, man_dep)   
            man_id_list.append(m.inde)

    if op == 't':
        dep = input('New Dep: ')
        id = input('Employee id: ')
        Employee.transfer(dep, int(id) )  

    if op == 'q':
        break          

    if op == 'f':
        id = input('Employee id: ') 
        Employee.fire(int(id)) 

    if op == 'l':
        Employee.list_employees() 

    if op == 's':
        id = input('Employee id: ') 
        
        
        for i in emp_id_list:
            if i == int(id):
                print(Employee.show(i))
                break    

        for im in man_id_list:
            if im == int(id):
                print(Manager.show(im))
                break     
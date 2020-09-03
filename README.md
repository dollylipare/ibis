# 1.Installation


Connecting to Oracle Exadata is possible only via the use of Oracle Database Wallet. The connector has been tested with the Autonomous Transaction Processing (ATP) Database set up on the Oracle Cloud Infrastructure. It makes use of the python library cx-oracle which is OSI approved BSD licensed library, conforming to Python DB API 2.0 specification. It needs the library installed as a dependency, where the connection will be made. Installation by pip can be executed using the following command:

`pip install cx-Oracle`

Additionally, Oracle Instant Client is a required dependency, which is available in the list of  Oracle Downloads. There are certain environment variables that need to be set, the list of which is available in the code snippet given below. These environment variables are related to discovery of the location of the Oracle Wallet for authorization of connection to Oracle Database. 

`TNS_ADMIN=<WALLET FOLDER PATH>`\
`LD_LIBRARY_PATH=<PATH TO ORACLE INSTANT CLIENT LIB>`

The Oracle Exadata client is accessible through the **ibis.sql.oracle namespace**.
The **ibis.sql.oracle.connect** with a SQLAlchemy compatible connection string to create a client connection
# 2.Code snippet for connecting to oracle Exadata using ibis:-

```sh
import ibis
import os
os.environ['TNS_ADMIN'] =  'wallet_folder_path'
# Example:-  os.environ['TNS_ADMIN'] = '/home/user_name/adb_virt_env'
from ibis.sql.ibis_oracle.api import connect 
db=connect("username","password","database")
tb_name=db.table("students")
result=tb_name.count().execute()
print(result)
```

# 3.Usage

+ **Important Note**

  In the "client.py" file make sure you update the "Wallet_Path_Location" in the code shown below:-
  ```
  os.environ['TNS_ADMIN'] = '<Wallet_Path_Location>'
  ```
+ **Schema for the ‘students_pointer’ table:-**
  ```
  CREATE TABLE students_pointer 
  ( 
     id              INTEGER, 
     name            VARCHAR(30), 
     division        INTEGER, 
     marks           INTEGER, 
     exam            VARCHAR(30), 
     overall_pointer FLOAT, 
     date_of_exam    TIMESTAMP 
  ); 
  ```

+ **Schema for the ‘awards’ table:-**
  ```
  CREATE TABLE awards 
  ( 
     id         INTEGER, 
     award_name VARCHAR(20) 
  ); 
  ```
+ **Queries showing implementation of different functions**
  ```
  import ibis
  from ibis.sql.ibis_oracle.api import connect
  con=connect("user_name","password","database_name")
  table_details=con.table('students_pointer')
  table_records=con.table('students_pointer').execute()

  # 3.1 Print the first two records of the table 'students_pointer'

    result_q1=table_details.limit(2).execute()
    print("Initial Two Records:\n " , result_q1)

  # 3.2 Print the highest scorers in each of the exams(biology,chemistry and maths)

    result_q2=table_details.group_by('exam').marks.max().execute()
    print(" Highest scorers in each of the exams:\n " , result_q2)

  # 3.3 Print the students in division “12” who have scored more than 490 marks

    cond1=table_details.division.isin([12])
    cond2=table_details.marks > 500
    result_q3=table_details.filter([cond1,cond2]).execute()
    print("Students(division=12 & marks>490 ):\n " , result_q3)

  # 3.4 Print the student records where division is sorted ascending manner and overall_pointer in descending manner

    from ibis import desc
    result_q4=table_details.sort_by(['division',desc(table_details.overall_pointer)]).execute()
    print("Result:\n " , result_q4)

  # 3.5 Selecting particular columns from the table
  
    result_q5=table_details.select(['name','marks']).execute()
    print("Result:\n " , result_q5)

  # 3.6 Perform the “Join operation” on the tables

    tb1=con.table('students_pointer')
    tb2=con.table('awards')

    join_expr = tb1.id==tb2.id
    joined = tb1.inner_join(tb2, join_expr)

    table_ref = joined[tb1, tb2.award_name.name('award_name')]
    result_q6=table_ref.select(['id','name','award_name']).execute()
    print("Print the students’ records who have won awards:\n " , result_q6)
    
  # 3.7 Write a query to find :-
        i.The minimum pointer, the maximum pointer, average pointer of students got in each of the three exams
        ii. Number of the people given the exam

         t = con.table('students_pointer')
         d = table_details.overall_pointer
         expr = (t.group_by('exam')
                  .aggregate([d.min(), d.max(), d.mean(), t.count()])
                  .sort_by('exam'))

        result_q7=expr.execute()
        print("Result:\n " , result_q7)


  # 3.8 Extract the information of students whose name starts with ‘R’

    result_q8= table_details[table_details.name.like('R%')].execute()
    print("Result:\n " , result_q8)

  # 3.9 Convert the values in “exam” Column into uppercase

    result_q9=table_details.select(['id','name',table_details.exam.upper()
                             .name('uppercase_letter')]).execute()
    print("Result:\n " , result_q9)


  # 3.10 Print the “year of the examination” for each of the students 

    result_q10=table_details[table_details.id,table_details.name,
                       table_details.date_of_exam,table_details.date_of_exam.year()
                       .name('year_of_exam')].execute()
    print("Result:\n " , result_q10)

  # 3.11 Print the number of unique names of exam
     
     t = con.table('students_pointer')
     result_q11=t.exam.nunique().execute()
     print("Result:\n " , result_q11)

  # 3.12 Print the distinct exam names

     t = con.table('students_pointer')
     result_q12=t.exam.distinct().execute()
     print("Result:\n " , result_q12)


  # 3.13 Print the name of students in the list/group format

    t = con.table('students_pointer')
    result_q13=t.name.group_concat().execute()
    print("Result:\n " , result_q13)

  # 3.14 Convert the values of timestamp column in the given format
  
    t=con.table('students_pointer')
    result_q14=t[t.date_of_exam.strftime('%Y%m%d %H').name('New_col')].execute()
    print("Result:\n " , result_q14)

  # 3.15 Extract the name and number of the day of the week from timestamp column
      
    t=con.table('students_pointer')

    result_q15=t[t.name,t.date_of_exam.day_of_week.index().name('weekday_number'),
                t.date_of_exam.day_of_week.full_name().name('weekday_name')].execute()
    print("Result:\n " , result_q15)
  ```



# 4.Steps to run Test scripts


+ **Schemas of the tables created in the database:**
  Create table named  “functional_alltypes” in the database with the below schema:-
  ```sh
  CREATE TABLE FUNCTIONAL_ALLTYPES
  ( 
     "index"         NUMBER(19), 
     "unnamed: 0"    NUMBER(19), 
     id              NUMBER(10), 
     bool_col        VARCHAR(4), 
     tinyint_col     NUMBER(5), 
     smallint_col    NUMBER(5), 
     int_col         NUMBER(10), 
     bigint_col      NUMBER(19), 
     float_col       FLOAT(23), 
     double_col      DOUBLE PRECISION, 
     date_string_col VARCHAR(10), 
     string_col      VARCHAR(10), 
     timestamp_col   TIMESTAMP, 
     year            INTEGER, 
     month           INTEGER 
   ); 
   ```

+ **Write the connection parameters(database credentials) in the following two files:-**
    * oracle/tests/udf/conftest.py
      ```sh
      OL_USER = os.environ.get(
      'IBIS_TEST_ORACLE_USER', os.environ.get('OLUSER', 'user_name')
      )
      OL_PASS = os.environ.get(
      'IBIS_TEST_ORACLE_PASSWORD', os.environ.get('OLPASSWORD', 'password')
      )
      IBIS_TEST_ORACLE_DB = os.environ.get(
      'IBIS_TEST_ORACLE_DATABASE', os.environ.get('OLDATABASE', 'database_name')
      )
      
      @pytest.fixture(scope='session')
      def con():
          ibis.sql.oracle.api.connect("user_name","password","database_name")
      ```
      
    * oracle/tests/udf/test_client.py
      ```sh
      ORACLE_TEST_DB=os.environ.get('IBIS_TEST_ORACLE_DATABASE','database_name')

      IBIS_ORACLE_USER = os.environ.get('IBIS_TEST_ORACLE_USER', 'user_name')

      IBIS_ORACLE_PASS = os.environ.get('IBIS_TEST_ORACLE_PASSWORD', 'password')
      ```

+ **To run individual test file:-**\
  ` pytest test_client.py`


+ **To run whole the test folder:-**\
  ` pytest tests/`





# 5.Limitations

Since ‘Boolean’ datatype is not supported in the oracle database few functions returning boolean value will not work.


# 6.  References
    
http://www.dominicgiles.com/blog/files/13ab9bba7c8831f42af87a01a150f3ce-172.html
https://www.oracle.com/database/technologies/instant-client/downloads.html



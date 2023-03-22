import pymysql
from datetime import date
from datetime import datetime

def get_connection():
    conn = pymysql.connect(host='localhost', user='squat_tester', password='squat_tester', db='squatdb', charset='utf8')
    if conn:
        print('DB connection complete')
    return conn

def get_squat_list(userNo):
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' select * from squattbl where userNo = %s'''
    cursor.execute(sql, userNo)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dict = {}
        temp_dict['num'] = row[0]
        temp_dict['quarter'] = row[2]
        temp_dict['half'] = row[3]
        temp_dict['full'] = row[4]
        temp_dict['total'] = row[5]
        temp_dict['date'] = row[6]
        temp_list.append(temp_dict)

    conn.close()
    return temp_list

def squat_add(userNo, s_quarter, s_half, s_full, s_total): #num/quarter/half/full/total
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' insert into squattbl values (null, %s, now(), %s, %s, %s, %s) '''

    cursor.execute(sql, (userNo, s_quarter, s_half, s_full, s_total))
    conn.commit()
    conn.close()


def search_result(s_date, userNo):
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' select * from squattbl where userNo = %s and datetime like %s '''
    search_date = s_date+'%'
    cursor.execute(sql, (userNo, search_date))
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dict = {}
        temp_dict['num'] = row[0]
        temp_dict['quarter'] = row[2]
        temp_dict['half'] = row[3]
        temp_dict['full'] = row[4]
        temp_dict['total'] = row[5]
        temp_dict['date'] = row[6]
        temp_list.append(temp_dict)

    sql = 'select sum(quarter), sum(half), sum(full), sum(total) from squattbl where userNo = %s and datetime like %s'
    cursor.execute(sql, (userNo, search_date))
    result = cursor.fetchall()[0]

    sum_list = []
    for i in result:
        if i == None:
            i=0
        sum_list.append(int(i))

    conn.close()
    return temp_list, sum_list

# Get the total number of squats and the number of each type
def get_sum_of_squat(userNo):
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'select sum(quarter), sum(half), sum(full), sum(total) from squattbl where userNo = %s'
    cursor.execute(sql, userNo)
    result = cursor.fetchall()[0]

    sum_list = []
    for i in result:
        if i ==None:
            i=0
        sum_list.append(int(i))

    conn.close()
    return sum_list

def get_sum_of_squat_with_date(s_date, userNo):
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'select sum(quarter), sum(half), sum(full), sum(total) from squattbl where userNo = %s and datetime like %s'
    search_date = s_date+'%'
    cursor.execute(sql, (userNo, search_date))
    result = cursor.fetchall()[0]
    sum_list = []
    for i in result:
        if i ==None:
            i=0
        sum_list.append(int(i))

    conn.close()
    return sum_list


def get_sum_of_challenge_squat(userNo, startdate, finishdate):
    conn = get_connection()
    cursor = conn.cursor()

    # sql = 'select sum(total) from squattbl where userNo = %s and date(datetime) = date(now())'
    sql = 'select sum(total) from squattbl where userNo = %s and date(datetime) between %s and %s'
    cursor.execute(sql, (userNo, startdate, finishdate))
    result = cursor.fetchall()[0][0]
    if result == None:  #Add an if statement?
        result = 0  

    conn.close()
    return result

# Get the number of squats in the current date-nday
def get_sum_of_squat_7days(nday, userNo):
    conn = get_connection()
    cursor = conn.cursor()
    sql = 'select left(now(),10)-interval %s day, sum(total) from squattbl where userNo = %s and left(datetime,10) = left(now(),10)-interval %s day'
    cursor.execute(sql,(nday,userNo,nday))
    result = cursor.fetchall()[0][1]
    if result == None:
        result = 0

    conn.close()
    return result



# Get full list of memberTBL tables
def get_member_list():
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' select * from membertbl order by userNo '''
    cursor.execute(sql)
    result = cursor.fetchall()

    temp_list = []
    for row in result:
        temp_dic = {}
        temp_dic['userNo'] = row[0]
        temp_dic['userName'] = row[1]
        temp_dic['userEmail'] = row[2]
        temp_dic['userPwd'] = row[3]
        temp_list.append(temp_dic)
    conn.close()
    return temp_list 

# Add member
def member_add(userName, userEmail, userPwd):
    conn = get_connection()
    cursor = conn.cursor()
    sql = '''
            insert into membertbl
                (userName, userEmail, userPwd)
                values (%s, %s, %s)
            '''
    cursor.execute(sql, (userName, userEmail, userPwd))
    conn.commit()
    conn.close()

# Returns 0 if userEmail does not exist, and returns that record if it exists.
def member(userEmail):
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''SELECT * FROM membertbl where userEmail = %s  '''
    cursor.execute(sql, userEmail)
    result = cursor.fetchone()
    if result:
        temp_dic = {}
        temp_dic['userNo'] = result[0]
        temp_dic['userName'] = result[1]
        temp_dic['userEmail'] = result[2]
        temp_dic['userPwd'] = result[3]
        conn.close()
        return temp_dic
    else:
        conn.close()
        return 0

 # return userNo
def userNo(userEmail):
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''SELECT userNo FROM membertbl where userEmail = %s  '''
    cursor.execute(sql, userEmail)
    result = cursor.fetchone()
    userNum = result[0]

    conn.close()
    return userNum

    
# userEmail, userPwd check function
def login_result(userEmail, userPwd):
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' select * from membertbl 
                where userEmail=%s and userPwd=%s '''
    cursor.execute(sql,(userEmail, userPwd))
    login_result = cursor.fetchone()

    if login_result:
        return True
    else:
        return False

# challenge
# Returns 0 if there is no challenge record, if so
def get_challenge(userNo):
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''SELECT * FROM challengetbl where userNo = %s  '''
    cursor.execute(sql,userNo)
    result = cursor.fetchone()
    if result:
        temp_dic = {}
        temp_dic['userNo'] = result[0]
        temp_dic['startdate'] = result[1]
        temp_dic['finishdate'] = result[2]
        temp_dic['count'] = result[3]
        conn.close()
        return temp_dic
    else:
        conn.close()
        return 0

# Challenge Update
def challenge_update(startdate,finishdate,count,userNo):
    conn = get_connection()
    cursor = conn.cursor()

    sql = '''UPDATE challengetbl SET startdate = %s, finishdate = %s, count = %s WHERE userNo = %s '''

    cursor.execute(sql, (startdate, finishdate, count, userNo))
    conn.commit()
    conn.close()

# Add Challenge
def challenge_add(userNo,startdate,finishdate,count):
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' insert into challengetbl values (%s, %s, %s, %s) '''

    cursor.execute(sql, (userNo, startdate, finishdate, count))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # temp_list = get_squat_list()
    # print(type(temp_list[1]['date']))
    # squat_add(3, 3, 3, 9, datetime.today())
    # print(get_squat_list())
    # print(search_result('2020-08-14'))
    # print(get_sum_of_squat())
    # print(get_sum_of_squat_with_date('2020-08-14'))
    # print(get_sum_of_today_squat())
    #print(get_sum_of_squat_7days('2'))
    # print(date.today())
    # print(type(date.today()))
    # print(get_sum_of_squat_7days(date.today()))
    #now = datetime.now()
    #print(now.year, now.month, now.day)
    # pre = datetime(20,9,29)
    # print(pre)
    # print(userNo('sungeun@naver.com'))
    print(get_sum_of_today_squat(2))

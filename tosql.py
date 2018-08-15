import pymysql
from datetime import datetime
def addUserData_to_Sql(UserID,Stock):
    now = datetime.now()
    conn = pymysql.Connect(host='pythondb.ceekfdzgubcw.ap-northeast-2.rds.amazonaws.com',
                        port = 3306,
                        user = 'root',
                        passwd = 'wldnjs0216',
                        database = 'UserInfo',
                        charset = 'utf8',
                        autocommit=True)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `%s`(`name` VARCHAR(100) NOT NULL,`search` VARCHAR(50) NOT NULL,`date` DATETIME NULL)"%UserID)
    cursor.execute("INSERT INTO `%s` VALUES('%s','%s','%s')"%(UserID,UserID,Stock,now))

    cursor.close()
    conn.close()


# 최근 검색 주식종목 한개 str 로 반환
def getRecentlySearch(UserID):
    conn = pymysql.Connect(host='pythondb.ceekfdzgubcw.ap-northeast-2.rds.amazonaws.com',
                        port = 3306,
                        user = 'root',
                        passwd = 'wldnjs0216',
                        database = 'UserInfo',
                        charset = 'utf8',
                        autocommit=True)
    cursor = conn.cursor()
    cursor.execute("SELECT `search` FROM `%s` ORDER BY `date` DESC "%UserID)
    rows = cursor.fetchone()

    tmp_str = rows[0]
    return(tmp_str)

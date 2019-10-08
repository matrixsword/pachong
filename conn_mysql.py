import pymysql

class Connection():
    def __init__(self):
        # 连接database
        self.conn = pymysql.connect(host="127.0.0.1",port =3306, user="root",password="toor",database="myvideo")
        # 得到一个可以执行SQL语句的光标对象
        self.cursor = self.conn.cursor()
    def add(self,data,category):
        #增
        sql = "INSERT INTO "+category+"(keyword, title, videourl, upname, flag) VALUES (%s, %s, %s, %s, %s);"
        try:
            # 批量执行多条插入SQL语句
            self.cursor.executemany(sql, data)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            # 有异常，回滚事务
            raise e

    def delete(self):
        #删
        sql = "DELETE FROM USER1 WHERE id=%s;"
        try:
            self.cursor.execute(sql, [4])
            # 提交事务
            self.conn.commit()
        except Exception as e:
            # 有异常，回滚事务
            self.conn.rollback()
    
    def update(self):
        #改
        sql = "UPDATE USER1 SET age=%s WHERE name=%s;"
        username = "Alex"
        age = 80
        try:
            # 执行SQL语句
            self.cursor.execute(sql, [age, username])
            # 提交事务
            self.conn.commit()
        except Exception as e:
            # 有异常，回滚事务
            self.conn.rollback()

    def search(self):                
        #查
        sql = "select * from meipai"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results  
            # for row in results :  
            #     id = row[0]    
        except Exception as e:  
            raise e

    def searchHaoKan(self):                
        #查
        sql = "select * from haokan"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results   
        except Exception as e:  
            raise e
    def searchHaoTu(self):                
        #查
        sql = "select * from haotu"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results    
        except Exception as e:  
            raise e
    def searchYiDian(self):                
        #查
        sql = "select * from yidian"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results   
        except Exception as e:  
            raise e
    def searchTianTian(self):                
        #查
        sql = "select * from tiantian"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results   
        except Exception as e:  
            raise e
    def searchQuTou(self):                
        #查
        sql = "select * from qutou"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results      
        except Exception as e:  
            raise e
    def searchDouYin(self):                
        #查
        sql = "select * from douyin"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results      
        except Exception as e:  
            raise e
    def searchSouHu(self):                
        #查
        sql = "select * from souhu"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results      
        except Exception as e:  
            raise e
    def searchWangYi(self):                
        #查
        sql = "select * from wangyi"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results      
        except Exception as e:  
            raise e
    def searchWeiBo(self):                
        #查
        sql = "select * from weibo"  
        try:  
            self.cursor.execute(sql)    #执行sql语句  
        
            results = self.cursor.fetchall()    #获取查询的所有记录  
            return results      
        except Exception as e:  
            raise e



    def get_one(self):
        # 获取单条查询数据
        sql = "SELECT id,name,age from USER1 WHERE id=1;"
        # 执行SQL语句
        self.cursor.execute(sql)

        ret = self.cursor.fetchone()
        self.cursor.close()
        self.conn.close()
        # 打印下查询结果
        print(ret)

    def get_all(self):
        # 获取多条查询数据
        sql = "SELECT id,name,age from USER1;"
        # 执行SQL语句
        self.cursor.execute(sql)

        ret = self.cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        # 打印下查询结果
        print(ret)
if "__main__" == __name__:
    conn = Connection()
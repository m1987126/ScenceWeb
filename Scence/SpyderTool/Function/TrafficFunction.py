import time
import csv
import pymysql
from SpyderTool.Tool.BaiduTraffic import BaiduTraffic
from SpyderTool.Tool.GaodeTraffic import GaodeTraffic
from SpyderTool.setting import *
from SpyderTool.setting import city_file_path, trafficdatabase
from concurrent.futures import ThreadPoolExecutor


class TraffciFunction(object):
    instance = None

    @staticmethod
    def initdatabase():

        db = pymysql.connect(host=host, user=user, password=password, database=trafficdatabase,
                             port=port)
        db.connect()
        cursor = db.cursor()
        with open(city_file_path, 'r') as f:

            read = csv.reader(f)
            read.__next__()
            for item in read:
                name = item[0]
                lat = float(item[1])
                lon = float(item[2])
                citycode = int(item[3])
                yearpid = int(item[4])
                sql = "insert into trafficdatabase.MainTrafficInfo(name,cityCode,bounds_lat,bounds_lon,yearPid) " \
                      "values ('%s','%d','%f','%f','%d')" % (name, citycode, lat, lon, yearpid)

                try:
                    cursor.execute(sql)
                    db.commit()
                except Exception as e:
                    print("error:%s" % e)
                    cursor.close()
                    db.rollback()
                    break
        cursor.close()
        db.close()
        return True

    @classmethod
    def dailycitytraffic(cls, citycodelist: list):
        while True:
            if cls.instance is None:
                cls.instance = super().__new__(cls)
            cls.instance.programmerpool(cls.instance.gettraffic, citycodelist)
            time.sleep(500)

    def gettraffic(self, citycode: int):
        db = pymysql.connect(host=host, user=user, password=password,
                             database=trafficdatabase,
                             port=port)

        if citycode > 1000:
            traffic = GaodeTraffic(db)

        elif 0 < citycode < 1000:

            traffic = BaiduTraffic(db)
        else:
            return
        t = time.time()
        today = time.strftime('%Y-%m-%d', time.localtime(t))
        yesterday = time.strftime('%Y-%m-%d', time.localtime(t - 3600 * 24))
        info = traffic.citytraffic(citycode)

        info = self.__dealwith_daily_traffic(info, citycode, db, today, yesterday)
        if info is None:
            print("Null")
            return None

        for item in info:
            date = item['date']
            index = float(item['index'])
            detailtime = item['detailTime']
            sql = "insert into  trafficdatabase.citytraffic(pid_id, date, trafficindex, detailtime)" \
                  " values('%d', '%s', '%s', '%s');" % (
                      citycode, date, index, detailtime)
            if not self.loaddatabase(db, sql):
                print("%s插入失败" % item)
                continue
        db.close()
        return True

    # 重复数据处理
    def __dealwith_daily_traffic(self, info, pid, db, today, yesterday):

        lis = []
        for item in info:
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        # 将昨天的数据全部剔除
        for i in range(len(info)):
            if info[i].get(yesterday) is None:
                info = info[i + 1:]
                break
        sql = "select  date,detailtime from trafficdatabase.CityTraffic where pid_id=" + str(
            pid) + " and date =str_to_date('" + today + "','%Y-%m-%d');"
        cursor = self.get_cursor(db, sql)
        if cursor is None:
            return None
        data = cursor.fetchall()
        cursor.close()
        # 剔除今天重复的数据
        for item in data:
            self.filter(info, item[0], item[1])
        lis.clear()
        # 字典反转回原来样子
        for item in info:
            lis.append(dict(zip(item.values(), item.keys())))
        info = lis
        return info

    def road_manager(self, citycode):
        db = pymysql.connect(host=host, user=user, password=password,
                             database=trafficdatabase,
                             port=port)

        t = time.localtime()
        date = time.strftime("%Y-%m-%d", t)
        detailtime = time.strftime("%H:%M", t)
        g = None
        if citycode > 1000:
            g = GaodeTraffic(db)
        elif citycode < 1000:
            g = BaiduTraffic(db)
        result = g.roaddata(citycode)
        if result is None:
            return None
        for item in result:
            sql = "insert into  trafficdatabase.RoadTraffic(pid_id,date,detailTime,name,direction," \
                  "speed,data,bounds,flag) " \
                  "values('%d','%s','%s','%s','%s','%f','%s','%s',%s);" % (
                      citycode, date, detailtime, item['RoadName'], item['Direction'], item['Speed'], item['Data'],
                      item['Bounds'], True)
            if not self.loaddatabase(db, sql):
                print("%s写入数据库失败" % item)
                continue
        print("success")
        db.close()
        return True

    def yeartraffic(self, citycode):
        db = pymysql.connect(host=host, user=user, password=password, database=trafficdatabase,
                             port=port)
        yearpid = self.__search_yearpid(citycode, db)
        g = None
        if yearpid > 1000:
            g = GaodeTraffic(db)
        elif yearpid < 1000:
            g = BaiduTraffic(db)
        result = g.yeartraffic(yearpid)
        result = self.__dealwith_year_traffic(result, yearpid, db,
                                              date=time.strftime("%Y-%m-%d",
                                                                 time.localtime(time.time() - 24 * 3600)))

        for item in result:
            date = item['date']
            index = item['index']
            city = item['city']
            sql = "insert into  trafficdatabase.YearCityTraffic(pid_id,date,city,TrafficIndex) " \
                  "values('%d','%s','%s','%f')" % (
                      citycode, date, city, index)
            if not self.loaddatabase(db, sql):
                print("%s写入数据库失败" % item)
                continue
        print("success")
        db.close()
        return True

    def __search_yearpid(self, citycode, db):
        sql = "select yearpid from trafficdatabase.MainTrafficInfo WHERE cityCode=" + str(citycode)

        cursor = self.get_cursor(db, sql)
        if cursor is None:
            print("查询失败")
            return None
        yearpid = cursor.fetchone()[0]
        if yearpid == 0:
            return citycode
        return yearpid

    def __dealwith_year_traffic(self, info, pid, db, date):
        sql = "select  date  from trafficdatabase.YearCityTraffic where pid_id=" + str(
            pid) + " and date >= '" + date + "'"
        cursor = self.get_cursor(db, sql)
        if cursor is None:
            print("年度数据查询日期数据失败！")
            return None
        try:
            result = str(cursor.fetchall()[-1][0])  # 最近的日期

        except IndexError:
            print("无相关重复数据，可以直接写入")
            return info
        info = list(info)
        i = 0
        for i in range(len(info)):
            if info[i]['date'] == result:
                break
        return info[i + 1:]

    # 写入数据库
    @staticmethod
    def loaddatabase(db, sql):

        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
            cursor.close()
        except Exception as e:

            print("error:%s" % e)
            db.rollback()
            cursor.close()
            return False
        return True

    # 性能提升
    @staticmethod
    def programmerpool(func, pidlist):
        tasklist = []

        threadpool = ThreadPoolExecutor(max_workers=6)

        for Pid in pidlist:
            task = threadpool.submit(func, Pid)
            tasklist.append(task)
        while [item.done() for item in tasklist].count(False):
            pass

    @staticmethod
    def get_cursor(db, sql):

        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print("查询错误%s" % e)
            db.rollback()
            cursor.close()
            return None
        return cursor

    # 数据过滤器
    @staticmethod
    def filter(info, date, detailtime):
        for i in range(len(info)):
            if info[i].get(str(date)) and info[i].get(detailtime):
                info.pop(i)
                return

# TraffciFunction().yeartraffic(119)

from sqlite3 import IntegrityError

import psycopg2
import traceback


class RelationalDBManager:

    def __init__(self):
        self.db_name = 'folks'
        self.user = 'postgres'
        self.host = 'localhost'
        self.password = 'geXDjm4Q'

    def execute_command(self, command):
        try:
            self.connection = psycopg2.connect("dbname='folks' user='postgres' host='localhost' password='geXDjm4Q'")
            self.cursor = self.connection.cursor()
            try:
                self.cursor.execute(command)
                resp = self.cursor.fetchall()
                self.cursor.close()
                return resp
            except psycopg2.Warning as warn:
                print command
                print warn
            except psycopg2.Error as err:
                print command
                print err.pgerror
            # finally:
            #     self.connection.rollback()
        except psycopg2.DatabaseError as e:
            print e.pgerror
        except Exception as ex:
            print "Exception occured: ", ex
        return None

    def execute_insert(self, command):
        try:
            self.connection = psycopg2.connect("dbname='folks' user='postgres' host='localhost' password='geXDjm4Q'")
            self.cursor = self.connection.cursor()
            try:
                self.cursor.execute(command)
                self.connection.commit()
                resp = self.cursor.statusmessage
                self.cursor.close()
                return resp
            except psycopg2.Warning as warn:
                print warn
            except psycopg2.Error as err:
                print err.pgerror
            finally:
                self.connection.rollback()
        except psycopg2.DatabaseError as e:
            print e.pgerror
        except Exception as ex:
            print "Exception occured: ", ex
        return None

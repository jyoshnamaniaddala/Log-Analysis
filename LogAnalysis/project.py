#!/usr/bin/env python3
import psycopg2
# name="news"


def connect_database():
    try:
        db_connect = psycopg2.connect("dbname=news")
        db_cursor = db_connect.cursor()
    except:
        print "specified database cannot be connected"
        return None
    else:
        return db_cursor, db_connect


def view_for_popular_articles(c, v):
    query = """create or replace view p_articles as select articles.title,
              count(*) as views from articles,log where
              log.path =concat('/article/',articles.slug)
              group by articles.title order by
              views desc;"""
    c.execute(query)
    v.commit()


def print_popular_articles(c, v):
    c.execute("select * from p_articles limit 3;")
    output = c.fetchall()
    v.commit()
    print "The most popular three articles"
    length = len(output)
    for i in range(0, length):
        print str(i+1)+"." + output[i][0] + "-" + str(output[i][1]) + " views"


def view_for_popular_authors(c, v):
    query = """create or replace view p_authors as select authors.name,
               count(*) as views from authors,log,articles where
               log.path =concat('/article/',articles.slug)
               and articles.author=authors.id
               group by authors.name order by
               views desc;"""
    c.execute(query)
    v.commit()


def print_popular_authors(c, v):
    c.execute("select * from p_authors limit 3;")
    output = c.fetchall()
    v.commit()
    print "The most popular article authors "
    length = len(output)
    for i in range(0, length):
        print (str(i+1)+"." + str(output[i][0]) +
               "-" + str(output[i][1]) + " views")


def finding_error_views(c, v):
    query = """create or replace view total_errors_views as select
             date(time) as date,count(*) as
             errors from log where status!='200 OK' group by
             date(time) order by errors desc;"""
    query1 = """create or replace view total_access_views as
              select date(time) as date,count(*) as access
               from log group by date(time)  order by access desc;"""
    query2 = """create or replace view error_percent_calculating as
              select total_access_views.date as Date,
               round((errors*100.00)/access,5) as percentage_error from
               total_access_views,total_errors_views  where
               total_access_views.date=total_errors_views.date order by
               percentage_error desc;"""
    c.execute(query)
    c.execute(query1)
    c.execute(query2)
    v.commit()


def print_per_error(c, v):
    c.execute("""select * from error_percent_calculating
                 where percentage_error>1.0;""")
    v.commit()
    output = c.fetchall()
    print "The days on which more than 1% of requests leads to errors "
    length = len(output)
    for i in range(0, length):
        print str(output[i][0]) + "---->" + str(output[i][1]) + "% errors"


if __name__ == '__main__':
    db_status, db_connect = connect_database()
    if db_status:
        print "connection established successfully"
        view_for_popular_articles(db_status, db_connect)
        print_popular_articles(db_status, db_connect)
        view_for_popular_authors(db_status, db_connect)
        print_popular_authors(db_status, db_connect)
        finding_error_views(db_status, db_connect)
        print_per_error(db_status, db_connect)
        db_connect.close()

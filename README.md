## Udacity Full Stack Web Developer Nanodegree-Logs Analysis Project ##
### PROJECT OVERVIEW ###
This is log analysis project  which requires students to find results from a large database of a news website using SQL quries.In this project views are created to analyse the results so that the original database need not to be disturbed,thus by using views we can find the result our quries.The primary objective of log analysis project is to extend the student's SQL database skills.

The database includes three tables:
* The **authors** table includes information about the authors of articles.
* The **articles** table includes information about the articles.
* The **log** table includes one entry for each time a user has accessed the site.

The python script is written to write quries and generate a report for the follwing questions:
   1. What are the most popular three articles of all time?
   2. Who are the most popular article authors of all time?
   3. On which days did more than 1% of requests lead to errors?
### TO RUN PROJECT ###
#### PreRequisites: ####

   * [Python3]
   * [Vagrant]
   * [VirtualBox]
#### To Setup Project : ####
1.Download [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).

2.If you don't have latest version of python,download and install it.

3.Download the data provided by Udacity [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

4.Unzip the file in order to extract newsdata.sql.

5.To bring virtual machine online `vagrant up`.

6.To login `vagrant ssh`.

7.Load the database using psql -d news -f newsdata.sql.

8.run the python file `samplefie.py`

#### Functions in samplefile.py: ####
* **connect_database():** Connects to the PostgreSQL database and returns a database connection.
* **view_for_popular_articles():** Function to Create view to find popular articles 
* **print_popular_articles():** Function to Prints the most popular three articles of all time.
* **view_for_popular_authors():** Function to Create view  to find popular authors 
* **print_popular_authors():** Function to Prints most popular article authors of all time.
* **finding_error_per_views():** Function to Create views,for finding error percentage.
* **print_per_error():** Function to Print days on which more than 1% of requests lead to errors.

#### VIEWS MADE : ####
QUERY 1 - VIEWS :
```
create or replace view p_articles as select articles.title,
              count(*) as views from articles,log where
              log.path =concat('/article/',articles.slug)
              group by articles.title order by
              views desc;
```
QUERY 2 - VIEWS :
```
create or replace view p_authors as select authors.name,
               count(*) as views from authors,log,articles where
               log.path =concat('/article/',articles.slug)
               and articles.author=authors.id
               group by authors.name order by
               views desc;
```
QUERY 3 - VIEWS :
```
create view total_errors_views as select
             date(time) as date,count(*) as
             errors from log where status!='200 OK' group by
             date(time) order by errors desc;

create view total_access_views as
              select date(time) as date,count(*) as access
               from log group by date(time)  order by access desc; 

create view error_percent_calculating as
              select total_access_views.date as Date,
               round((errors*100.00)/access,5) as percentage_error from
               total_access_views,total_errors_views  where
               total_access_views.date=total_errors_views.date order by
               percentage_error desc;
```
### OUTPUT ###
```
connection established successfully
The most popular three articles
1.Candidate is jerk, alleges rival-338647 views
2.Bears love berries, alleges bear-253801 views
3.Bad things gone, say good people-170098 views

The most popular article authors
1.Ursula La Multa-507594 views
2.Rudolf von Treppenwitz-423457 views
3.Anonymous Contributor-170098 views

The days on which more than 1% of requests leads to errors
2016-07-17---->2.26269% errors
```



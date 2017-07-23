Instructions
============

The rest of the tabs have customer data in the structure from our database.

The name of each tab is the name of that table and the primary key of each table is highlighted in yellow.

Fields to join on should be self-explanatory. You can assume the TABLE.x_id is the same as x.id. Just make reasonable assumptions and move forward.

Questions
=========

**1. Write a SQL query to join all of the tables into one large view.**

> Written assuming a MySQL database.
> This code doesn't have every column of every table, since that wouldn't be very useful. 
> Instead, we have *most* of the columns with meaningful information displayed.
> It is organized first by user information, then order information. The last column, "subsidy", should just say whether the order was subsidized, based on what day of week the order was made.
> All six of the tables are used to create this view. 

        select
            company_id, user_id, joined_date, is_admin,
            location_id, o.id as order_id, order_datetime, delivery_date, status, auto_order, source, 
            restaurant_name, name, temperature, value, 
            case when dayofweek(delivery_date) = 2 then mon_subsidy 
                when dayofweek(delivery_date) = 3 then tue_subsidy
                when dayofweek(delivery_date) = 4 then wed_subsidy 
                when dayofweek(delivery_date) = 5 then thu_subsidy 
                when dayofweek(delivery_date) = 6 then fri_subsidy 
                else null end as subsidy
         from users as u 
         left join orders as o on (o.user_id = u.id)
         left join items_ordered as io on (o.id = io.order_id)
         left join items as i on (io.item_id = i.id)
         left join tags as t on (t.item_id = i.id)
         left join payment_groups as pg on (o.payment_group_id = pg.id)
        ;

>After creating this query, I then saved it as a view so it could be accessed 
>easily.

**2. Examine a few trends in ordering behavior and summarize a couple of interesting things.**
> *Please refer to analysis.ipynb for more in-depth analysis.*

 - Most orders are placed on Mondays. There are troughs during national holidays, but there are also a few mysterious surges in orders on January 9th, January 24th, and February 28th.
 - About 10% of orders from January through March are cancelled. That's high.
 - All of the cancellations in this dataset are done by four out of the ten listed companies.
 - The five most-used tags are

**3. Based on your findings, make a business recommendation for a specific part of the company and justify why you'd reccommend that.**

- Send a survey to the companies who cancel their orders frequently to find out why they tend to cancel at such a high rate. This will help EAT club understand why cancellations happen, and perhaps make product decisions in light of that information in order to keep cancellations to a minimum.

**4. After looking at the above questions, what data would you be most interested in adding to the analysis? How would you measure them?**

- With regard to companies that cancel frequently, loading the survey results (if a survey is sent out) into the database and implementing tagging for why a cancellation occured would help EAT Club avoid costs associated with cancellations.

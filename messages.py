from db import db
import users 
from sqlalchemy import text
import pandas as pd
import plotly.express as px

def front_page_view(): 
    user_id = users.user_id()
    if user_id == 0:
        raise ValueError("User ID is 0. Redirect to login")
    
    sql_1 = text("SELECT C.id, C.name, S.sex, C.language, A.age_group, C.phone, C.email FROM customer C, sex S, age A WHERE C.sex_id = S.id AND C.age_group_id = A.id ORDER BY C.id")
    result_1 = db.session.execute(sql_1)
    customers = result_1.fetchall()

    sql_2 = text("SELECT COUNT(id) from customer")
    result_2 = db.session.execute(sql_2)
    number = result_2.fetchone()[0]

    return customers, number

def new_customer_registration(name, sex, language, age_group, phone, email):
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    sql = text("INSERT INTO customer (name, sex_id, language, age_group_id, phone, email) VALUES (:name, :sex, :language, :age_group, :phone, :email) RETURNING id") 
    db.session.execute(sql, {"name":name, "sex":sex, "language":language, "age_group":age_group, "phone":phone, "email":email})
    db.session.commit()

    return True

def customer_name(id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    sql = text("SELECT name FROM customer WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]

    return id,name

def new_meeting_registration(date,service_id,customer_id,customer_path,realization_id,execution_id,notes):
    user_id = users.user_id()

    sql = text("INSERT INTO meeting (date, service_id, user_id, customer_id, customer_path, realization_id, execution_id, notes) VALUES (:date, :service_id, :user_id, :customer_id, :customer_path, :realization_id, :execution_id, :notes) RETURNING id")
    db.session.execute(sql, {"date":date, "service_id":service_id, "user_id":user_id, "customer_id":customer_id, "customer_path":customer_path, "realization_id":realization_id, "execution_id":execution_id, "notes":notes})
    db.session.commit()

    return True

def see_notes(id):
    sql_1 = text("SELECT M.date, M.service_id, U.username, M.customer_path, M.realization_id, M.execution_id, M.notes FROM meeting M, customer C, users U WHERE C.id = :id AND M.customer_id = C.id AND M.user_id = U.id")
    result_1 = db.session.execute(sql_1, {"id":id})
    notes = result_1.fetchall()

    sql_2 = text("SELECT COUNT(C.id) FROM meeting M, customer C, users U WHERE C.id = :id AND M.customer_id = C.id AND M.user_id = U.id")
    result_2 = db.session.execute(sql_2, {"id":id})
    number = result_2.fetchone()[0]

    return notes,number

def customer_modification(id, name, sex, language, age_group, phone, email):
    user_id = users.user_id()
    if user_id == 0:
        return False

    if not id:
        return False

    sql = text("UPDATE customer SET name = :name, sex_id = :sex, language = :language, age_group_id = :age_group, phone = :phone, email = :email WHERE id = :id")
    db.session.execute(sql, {"name": name, "sex": sex, "language": language, "age_group": age_group, "phone": phone, "email": email, "id": id})
    db.session.commit()

    return True

def meeting_numbers():
    sql = text("""
        SELECT
            COUNT(CASE WHEN realization_id = 1 THEN 1 END) AS called_count,
            COUNT(CASE WHEN realization_id = 2 THEN 1 END) AS canceled_count
        FROM meeting;
    """)
    
    result = db.session.execute(sql)
    counts = result.fetchone()
    called_count = counts[0] 
    canceled_count = counts[1] 

    return called_count, canceled_count

def plots(realization,service,start_date,end_date,execution_style):
    user_id = users.user_id()
    if user_id == 0:
        return False
    
    sql = text(f"SELECT S.sex as customer_sex, C.language, A.age_group as customer_age, M.date as  meeting_date, E.service, R.realization as did_it_happen, X.execution FROM sex S, customer C, age A, meeting M, service E, realization R, execution X WHERE C.sex_id = S.id AND C.age_group_id = A.id AND C.id = M.customer_id AND M.service_id = E.id AND M.realization_id = R.id AND M.execution_id = X.id AND M.realization_id IN ({realization}) AND M.service_id IN ({service}) AND M.date >= '{start_date}' AND M.date <= '{end_date}' AND M.execution_id IN({execution_style})")
    result = db.session.execute(sql) # Miksi tähän ei mene sulkeisiin sisään {"name":name, "sex":sex} jne ??
    data = result.fetchall()
    
    df = pd.DataFrame(data, columns=['Sex','Language','Age group','Meeting date','Service','Realization style','Execution style'])

    # Converting 'Meeting date' to datetime format
    df['Meeting date'] = pd.to_datetime(df['Meeting date'])

    ## First plot:

    # Group by 'Meeting date' and 'Service', count total sexes
    grouped_df_0 = df.groupby(['Meeting date', 'Service'])['Sex'].count().reset_index(name='Count')

    fig_scatter_0 = px.scatter(grouped_df_0, x="Meeting date", y="Count", color="Service", size="Count", title=f'Meeting progression between {start_date} to {end_date}',
                         labels={'Count': 'Number of Customers'}, size_max=10)
    
    # Save the HTML plot to a variable
    pic_0 = fig_scatter_0.to_html(full_html=False)

    ## Second plot:

    grouped_df_1 = df.groupby(["Service", "Sex"]).size().reset_index(name='Count')

    grouped_df_1['marker_size'] = 20  # Set the size for the "balls"

    fig_scatter_1 = px.scatter(grouped_df_1, x="Service", y="Count", color="Sex", size="marker_size")

    fig_scatter_1.update_layout(
        title=f"Count of Customers by Service and Gender From {start_date} To {end_date}",
        xaxis_title="Service(s) selected",
        yaxis_title="Number of Customers"
                            )

    pic_1 = fig_scatter_1.to_html(full_html=False)

    ## Third plot:

    grouped_df_2 = df.groupby(["Language", "Execution style"]).size().reset_index(name='Count')

    grouped_df_2['marker_size'] = 20  

    fig_scatter_2 = px.scatter(grouped_df_2, x="Language", y="Count", color="Execution style", size="marker_size")

    fig_scatter_2.update_layout(
        title=f"Count of Customers by Language and Style of the Meeting From {start_date} To {end_date}",
        xaxis_title="Languages",
        yaxis_title="Number of Customers"
                            )

    pic_2 = fig_scatter_2.to_html(full_html=False)

    ## Returning 3 plots

    return pic_0, pic_1, pic_2

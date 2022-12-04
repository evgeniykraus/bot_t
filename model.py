from conn import connection


def find_phone_number(phone):
    answer = list()
    get_phone = f"select * from SUBSCRIBERS where phone = '{phone}'"
    with connection.cursor() as cursor:
        cursor.execute(get_phone)
        result = cursor.fetchall()
        for row in result:
            answer.append({"id": row[0], "surname": row[1], "name": row[2], "patronymic": row[3], "phone": row[4]})
    return answer


def get_all_subscribers():
    answer = list()
    get_subscribers = "select * from SUBSCRIBERS"
    with connection.cursor() as cursor:
        cursor.execute(get_subscribers)
        result = cursor.fetchall()
        for row in result:
            answer.append(f'{row[1]} {row[2]} {row[3]} {row[4]}')
    return answer


def insert_sub(subscriber):
    insert_subscriber = f'INSERT INTO SUBSCRIBERS (surname, name, patronymic, phone) VALUES ({subscriber})'
    with connection.cursor() as cursor:
        cursor.execute(insert_subscriber)
        connection.commit()


def find_subscriber(sub_data):
    sub_data = f"SELECT * FROM `SUBSCRIBERS`  WHERE CONCAT(surname , name, patronymic, phone) LIKE '%{sub_data}%'"
    answer = list()
    with connection.cursor() as cursor:
        cursor.execute(sub_data)
        result = cursor.fetchall()
        for row in result:
            answer.append(f'{row[1]} {row[2]} {row[3]} {row[4]}')
        return answer


def dell_subscriber(phone):
    sub_data = f"DELETE FROM `SUBSCRIBERS` WHERE phone = '{phone}'"

    with connection.cursor() as cursor:
        cursor.execute(sub_data)
        connection.commit()
    return True


def truncate_table_subscribers():
    sub_data = f"truncate table `SUBSCRIBERS`"

    with connection.cursor() as cursor:
        cursor.execute(sub_data)
        connection.commit()
    return True

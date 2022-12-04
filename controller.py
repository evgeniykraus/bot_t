import model
import re


def get_all_subscribers():
    result = model.get_all_subscribers()
    return result


def check_input_data(data):
    try:
        result = re.match(r'^[А-я]{1,20}$', data).string.capitalize()
        return result
    except:
        return False


def phone_number(phone):
    try:
        result = re.match(r'^((\+7|7|8)+([0-9]){10})$', re.sub('[\s |^+]', '', phone)).string
        result = re.sub(r"^8", "7", result)

        if len(model.find_phone_number(result)) != 0:
            return -1
        else:
            return result
    except:
        return False


def add_new_sub(subscriber):
    try:
        subscriber = subscriber.split(" ")
        result = phone_number(f"{subscriber[3]}")
        if result == -1:
            return result
        else:
            model.insert_sub(
                f"'{subscriber[0].capitalize()}', '{subscriber[1].capitalize()}', '{subscriber[2].capitalize()}', '{result}'")
            return True
    except:
        return False


def get_subscriber_data(data):
    result = model.find_subscriber(data.replace(' ', ''))
    return result


def dell_sub(phone):
    try:
        model.dell_subscriber(phone)
        return True
    except:
        return False


def truncate_table():
    return model.truncate_table_subscribers()
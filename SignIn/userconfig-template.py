from datetime import time

# administrator of the sign_in_model
admin_whitelist = {123456789}

# The id of the group
target_group = 123456789

signin_time_start = time(hour=18, minute=45)
signin_time_stop = time(hour=19, minute=20)

# time to remind members to sign in
signin_time_remind = time(hour=18, minute=55)
# time to warn members which have not submitted status yet
signin_time_warning = time(hour=19, minute=10)

# sign in schedule of weekdays
# Monday == 0 ... Sunday == 6
sign_schedule = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
}

qq_to_name = {
    123456789: "user_name",
}


name_to_qq = dict([(qq_to_name[qq], qq) for qq in qq_to_name])
name_list = {qq_to_name[qq] for qq in qq_to_name}
qq_list = {qq for qq in qq_to_name}

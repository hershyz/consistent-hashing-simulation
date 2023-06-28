import styles
import load_balancer
import user_storage

commands = {'add_servers', 'add_users', 'remove_users', 'remove_users'}

percentage_codes = {
    (0, 32): styles.COLOR_GREEN,
    (33, 66): styles.COLOR_YELLOW,
    (67, 100): styles.COLOR_RED
} # interval (inclusive) : percentage display color

def display_help():
    print('')
    print(styles.FORMAT_BOLD + styles.COLOR_RED + 'malformed command' + styles.FORMAT_RESET)
    print('--------------')
    print(styles.FORMAT_BOLD + 'valid commands:' + styles.FORMAT_RESET)
    print('add_servers ' + styles.COLOR_MAGENTA + '[n]' + styles.FORMAT_RESET)
    print('add_users ' + styles.COLOR_MAGENTA + '[n]' + styles.FORMAT_RESET)
    print('remove_servers ' + styles.COLOR_MAGENTA + '[n]' + styles.FORMAT_RESET)
    print('remove_users ' + styles.COLOR_MAGENTA + '[n]' + styles.FORMAT_RESET)
    print('')

def get_percentage_code(percentage):
    for interval in percentage_codes:
        if percentage >= interval[0] and percentage <= interval[1]:
            return percentage_codes[interval]

def cli_loop():

    command = input(styles.COLOR_YELLOW + '> ' + styles.FORMAT_RESET).split(' ')

    # malformed command
    malformed_command = False
    malformed_args = False
    if command[0].lower() not in commands:
        malformed_command = True
    try:
        int(command[1])
    except:
        malformed_args = True
    if malformed_command or malformed_args:
        display_help()

    # well-formed command
    if not malformed_command and not malformed_args:
        if command[0].lower() == 'add_servers': load_balancer.add_servers(int(command[1]))
        if command[0].lower() == 'add_users': user_storage.add_users(int(command[1]))
        if command[0].lower() == 'remove_servers': load_balancer.remove_servers(int(command[1]))
        if command[0].lower() == 'remove_users': user_storage.remove_users(int(command[1]))
    
    # display servers and load (if command is well-formed)
    if not malformed_command and not malformed_args:

        load_balancer.route_requests()
        print('')
        print(styles.FORMAT_BOLD + 'server ID | request mod space | server load' + styles.FORMAT_RESET)

        n_users = len(user_storage.uuids)
        for i in range(len(load_balancer.server_ring)):
            
            s = load_balancer.server_ring[i]
            request_mod_range = [0, 0]
            if i > 0:
                request_mod_range[0] = load_balancer.server_ring[i - 1].request_handling_threshold + 1
            request_mod_range[1] = s.request_handling_threshold
            
            n_handled = len(s.clients)
            percentage = (n_handled / n_users) * 100
            percentage = round(percentage, 2)
            color_code = get_percentage_code(percentage)
            
            print(str(s.server_id) + ' | ' + str(request_mod_range) + ' | ' + color_code + str(percentage) + '%' + styles.FORMAT_RESET)

        print('')
    
    cli_loop()
    
cli_loop()
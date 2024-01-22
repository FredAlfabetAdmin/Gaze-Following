# Pretty prints the current stage in the terminal
def show_current_stage(value):
    string_func = lambda x: ''.join(["=" for _ in range(len(x))])
    print("")
    print(f"====={string_func(value)}=====")
    print(f"===  {value}  ===")
    print(f"====={string_func(value)}=====")

# Determines for the first item if which direction it has to go.
def left_or_right(congruent, direction):
    if (congruent and direction == 'left') or (not congruent and direction == 'right'):
        return 'left'
    else: 
        return 'right'
        
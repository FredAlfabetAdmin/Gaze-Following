def show_current_stage(value):
    string_func = lambda x: ''.join(["=" for _ in range(len(x))])
    print("")
    print(f"====={string_func(value)}=====")
    print(f"===  {value}  ===")
    print(f"====={string_func(value)}=====")
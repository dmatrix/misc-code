import inspect
import varfuncs

if __name__ == '__main__':
    [print(name) for name in inspect.getmembers(varfuncs, inspect.isclass)]
    [print(name) for name in inspect.getmembers(varfuncs, inspect.isfunction)]
    print("-" * 50)
    func_list = [func for name, func in
                 inspect.getmembers(varfuncs, inspect.isfunction)]
    print(func_list)


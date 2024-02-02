class Class:
    class_variable: int = 0

    def __init__(self, value):
        self.instance_variable = value
    
if __name__ == "__main__":
    obj_1 = Class(5)
    obj_2 = Class(5)

    print(f"Class variable: {Class.class_variable}")
    print(f"obj_1 class varialbe: {obj_1.class_variable}")
    print(f"obj_2 class varialbe: {obj_2.class_variable}")

    # change instance class variable
    obj_1.class_variable = -5

    print("--" * 10)
    print(f"Class variable: {Class.class_variable}")
    print(f"obj_1 class varialbe: {obj_1.class_variable}")
    print(f"obj_2 class varialbe: {obj_2.class_variable}")

    # Change global class variable
    Class.class_variable = 20

    print("--" * 10)

    print(f"Class variable: {Class.class_variable}")
    print(f"obj_1 class varialbe: {obj_1.class_variable}")
    print(f"obj_2 class varialbe: {obj_2.class_variable}")
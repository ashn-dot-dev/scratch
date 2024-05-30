# bug.mojo

fn print_borrowed_arg1[T: Stringable](borrowed value: T):
    print(value)

fn print_borrowed_arg2[T: Stringable](borrowed value: T):
    print("arg1", value)

fn print_borrowed_arg3[T: Stringable](borrowed value: T):
    print("arg1", "arg2", value)

fn print_owned_arg1[T: Stringable](owned value: T):
    print(value)

fn print_owned_arg2[T: Stringable](owned value: T):
    print("arg1", value)

fn print_owned_arg3[T: Stringable](owned value: T):
    print("arg1", "arg2", value)

fn print_inout[T: Stringable](inout value: T):
    print("print_inout:", value)

fn print_borrowed1[T: Stringable](owned value: T):
    print("print_borrowed1:", value)

fn print_borrowed2[T: Stringable](owned value: T):
    print("print_borrowed2: ", end="")
    print(value)

fn print_owned1[T: Stringable](owned value: T):
    print("print_owned1:", value)

fn print_owned2[T: Stringable](owned value: T):
    print("print_owned2: ", end="")
    print(value)

@value
@register_passable
struct Vec2:
    var x: Float32
    var y: Float32

    fn __str__(self) -> String:
        return String("Vec2(x=") + self.x + ", y=" + self.y + ")"

@value
struct Person:
    var first_name: String
    var last_name: String

    fn __str__(self) -> String:
        return self.first_name + " " + self.last_name;

fn main():
    print("Short Summary")
    print_borrowed_arg1(String("abc"))
    print_borrowed_arg2(String("abc"))
    print_borrowed_arg3(String("abc"))
    var owned1 = String("abc")
    var owned2 = String("abc")
    var owned3 = String("abc")
    print_owned_arg1(owned1)
    print_owned_arg2(owned2)
    print_owned_arg3(owned3)

    print("", end="\n")

    print("Int")
    var i = 123
    print_inout(i)
    print_borrowed1(123)
    print_borrowed2(123)
    print_owned1(123)
    print_owned2(123)

    print("", end="\n")

    print("String")
    var s = String("abc")
    print_inout(s)
    print_borrowed1(String("abc"))
    print_borrowed2(String("abc"))
    print_owned1(String("abc"))
    print_owned2(String("abc"))

    print("", end="\n")

    print("Vec2 (register passable)")
    var v = Vec2(123.0, 456.0)
    print_inout(v)
    print_borrowed1(Vec2(123.0, 456.0))
    print_borrowed2(Vec2(123.0, 456.0))
    print_owned1(Vec2(123.0, 456.0))
    print_owned2(Vec2(123.0, 456.0))

    print("", end="\n")

    print("Person (not register passable)")
    var p = Person("Ada", "Lovelace");
    print_inout(p)
    print_borrowed1(Person("Ada", "Lovelace"))
    print_borrowed2(Person("Ada", "Lovelace"))
    print_owned1(Person("Ada", "Lovelace"))
    print_owned2(Person("Ada", "Lovelace"))

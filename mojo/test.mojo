# Working through the Mojo manual.
#
# $ python3 -m venv mojo-venv && source mojo-venv/bin/activate
# $ mojo --version
# mojo 24.3.0 (9882e19d)

fn greeting(name: String) -> String:
    return "Hello, " + name + "!";

fn greet(name: String):
    print(greeting(name))

fn add_one(value: Int) -> Int:
    var one: Int = 1;
    return value + one;

fn take_ownership_and_print[T: Stringable](owned x: T):
    print("take ownership and print:", x)

@value
struct Pair:
    var first: Int
    var second: Int

    fn dump(self):
        # XXX: Mojo does not support f-strings 😕
        print("Pair(first=" + String(self.first) + ", second=" + String(self.second) + ")")

trait Dumpable:
    fn dump(self): ...

fn dump[T: Dumpable](x: T):
    x.dump()

fn repeat[count: Int](msg: String):
    for i in range(count):
        print(msg)

fn sum(*values: Int) -> Int:
    var result = 0
    for v in values:
        result += v
    return result

# XXX: This currently does not work 😕
#fn cat(*strings: String) -> String:
#    return "".join(strings)

# XXX: This also does not seem to work when called with:
#    make_worldly("Hello", "Big ol'")
#
# or
#
#    var strings = ("Hello", "Big ol'")
#    make_worldly(strings)
#
# or
#
#    var strings = ["Hello", "Big ol'"]
#    make_worldly(strings)
#
# or any combination of those using String() constructors. The ergonomics and
# error messages here are not great. It is not obvious how to create a value
# that could be mutable passed to make_worldly, despite the documentation using
# this function. 😕
#
#fn make_worldly(inout *strs: String):
#    # Requires extra [] to dereference the reference for now.
#    for i in strs:
#        i[] += " world"

# XXX: Calling this function with:
#
#   print(sum_heterogeneous(1, 2.5, 3))
#
# behaves as expected. But calling the function as:
#
#   print(sum_heterogeneous(1, 2.5, "3"))
#
# produces the error:
#
#   error: invalid call to 'sum_heterogeneous': callee with non-empty variadic pack argument expects 0 positional operands, but 3 were specified
#       print(sum_heterogeneous(1, 2.5, "3"))
#
# which is odd. My guess is that String or StringLiteral isn't Intable even
# though `int("3")` works just fine, and it leads to some sort of weird
# internal compiler error where the arguments have not yet been marked as part
# of the variadic argument pack. Either that or I am just totally reading this
# error message wrong.
fn sum_heterogeneous[*T: Intable](*args: *T) -> Int:
    var result = 0

    @parameter
    fn add[Ty: Intable](borrowed value: Ty):
        result += int(value)

    args.each[add]()
    return result

# XXX: I originally wrote the print statment here as:
#
#   print(k[], "=", args[k])
#
# and forgot the `[]` in `k[]` which produced the error:
#
#   error: invalid call to '__getitem__': index cannot be converted from 'Reference[String, 0, (mutcast mut args), 0]' to 'String'
#           print(k[], "=", args[k])
#                           ~~~~^~~
#
# which indicated the error, but oh boy was it verbose an unergonomic. This
# sounds like a simple enough case where the compiler could infer that I
# probably wanted to write `k[]`.
fn print_nicely(**args: Int) raises:
    for k in args.keys():
        print(k[], "=", args[k[]])

fn double_mutable_reference(inout x: Int, inout y: Int):
    x += 1
    y += 1

fn mutable_reference_and_immutable_reference(inout x: Int, borrowed y: Int):
    x += 1

fn drop[T: Stringable](owned x: T):
    print("dropping: ", end="") # XXX: Workaround for print("text", x) not working 😕
    print(x)

trait Introduceable:
    # Compiler error:
    #
    #   error: TODO: fields in traits are not supported yet
    #
    # Have to define a `get_name` method as part of this implementation.
    #var name: String

    # I wish we had explicit lifetimes so that I could retun a string reference
    # with the same lifetime as self:
    #
    #   fn get_name['a](owned 'a self) -> 'a String
    fn get_name(self) -> String: ...
    fn introduce(self): ...

@value
struct Robot(Introduceable):
    var name: String

    fn get_name(self) -> String:
        return self.name

    fn introduce(self):
        print("beep, boop, my name is", self.name, "the robot")

@value
struct Dragon:
    var name: String

    fn get_name(self) -> String:
        return self.name

    # Implicitly implements Introduceable.
    fn introduce(self):
        print("rawr, my name is", self.name, "the dragon")

fn introduction[T: Introduceable](x: T):
    print("Introducing their excellence,", x.get_name())
    print("> ", end="")
    x.introduce()

def main():
    greet("ashn")
    print("123 + 1 = " + String(add_one(123)))
    var pair = Pair(123, 456)
    pair.dump()
    var pair1 = pair
    pair1.first = 789
    print("Dumping `pair`")
    dump(pair)
    print("Dumping `pair1`")
    dump(pair1)
    repeat[3]("hello")
    print(sum(123, 456, 789))
    #print(cat("abd", "def", "hij"))
    #make_worldly(String("Hello"), String("Big ol'"))
    print(sum_heterogeneous(1, 2.5, 3))
    #print(sum_heterogeneous(1, 2.5, "3"))
    print_nicely(a=123, c=789, b=456)

    # Late initialize a variable, but never assign it before use.
    var late: String
    # Uncommenting the line below will give the error:
    #
    #   error: use of uninitialized value 'late'
    #
    # Nice! Glad this does not pass semantic analysis.
    #print(late)

    # Nice, I can only use late if all branches seem to assign late!
    from random import seed, random_ui64
    seed(123)
    if random_ui64(0, 1) == 0:
        late = "Now I am assigned (if-branch)!"
    elif random_ui64(0, 1) == 0:
        late = "Now I am assigned (elif-branch)!"
    else:
        late = "Now I am assigned (else-branch)!"
    print(late)

    # Nice, this also does not work!
    # Additional note, and extra error:
    #
    #   mojo: error: failed to run the pass manager
    #
    # is printed after the error about an uninitialized variable. This probably
    # should not be printed.
    #var late1: String
    #while random_ui64(0, 1) == 0:
    #    late1 = "Now I am assigned (while)!"
    #print(late1)

    # Nice, the compiler knows that this branch will always be executed and
    # will let me use late2 in the print statement below.
    var late2: String
    while True:
        late2 = "Now I am assigned (while-true)!"
        break
    print(late2)

    # Assignment using overloaded single-argument is a *really* good idea, and
    # is especially nice in a python-esque language.
    var implicit_cast_from_int_to_string: String = 123
    print("implicit_cast_from_int_to_string =", implicit_cast_from_int_to_string)
    # I think the implicit cast for function arguments is less good, I feel
    # like this leads to the same overload "what the heck types are being
    # constructed" headache that you get in C++ when you fail to mark
    # everything as `explicit`.
    fn printstr(s: String):
        print("printing string:", s)
    printstr(123) # 😕

    # The docs have this blurb under the "Ownership Summary" section[1]:
    #
    # > You cannot create a mutable reference (inout) if there exists an
    # > immutable reference (borrowed) for the same value. (TODO: Not currently
    # > implemented.)
    #
    # which seems *really* bad. Like this breaks the whole point of having
    # Rust-style single-ownership rules.
    # [1]: https://docs.modular.com/mojo/manual/values/ownership#ownership-summary
    var x = 123
    var y = 456
    print("x = ", x);
    print("x = ", y);
    print("calling double_mutable_reference(x, y)");
    double_mutable_reference(x, y)
    print("x = ", x);
    print("x = ", y);
    var z = 789
    print("z = ", z);
    print("calling double_mutable_reference(z, z)");
    double_mutable_reference(z, z) # Yikes!!
    print("z = ", z);
    print("calling mutable_reference_and_immutable_reference(z, z)");
    mutable_reference_and_immutable_reference(z, z) # Yikes!!
    print("z = ", z);

    take_ownership_and_print(123)
    take_ownership_and_print("some string")
    var owned_string1 = String("owned string 1")
    var owned_string2 = String("owned string 2")
    # Uhhh... I think there is a bug here 😕. Currently this gets printed:
    #
    #   take ownership and print: 
    #   take ownership and print: 
    #
    # when I should be seeing:
    #
    #   take ownership and print: owned string 1
    #   take ownership and print: owned string 2
    #
    # This is double weird because if you add a `print(x)` inside
    # `take_ownership_and_print` by itself the value does get printed.
    take_ownership_and_print(owned_string1) # copied
    take_ownership_and_print(owned_string2^) # transferred
    print("still owned:", owned_string1) # Can use after because owned_string1 was not transferred.
    # Compiler prevents me from using a moved value! Yay!
    # But the error message is weird:
    #
    # > error: use of uninitialized value 'owned_string2'
    # > print(owned_string2)
    # >      ^
    #
    # this probably should say something like "value was moved here" and point
    # to the call to `take_ownership_and_print`.
    #print(owned_string2)

    # This (expectedly) does not compile, but again the error messages are not
    # great, referring to an uninitialized value rather than a lifetime issue.
    #var s = String("abc")
    #if True:
    #    drop(s^)
    #else:
    #    pass
    #print(s)

    # XXX: Using something like:
    #
    #   var robot: Robot = "Bob"
    #
    # will produce the error:
    #
    #   error: cannot implicitly convert 'StringLiteral' value to 'Robot' in 'var' initializer
    #
    # Since StringLiteral can be converted to String, I would sort of expect
    # this to work from a C++ background, but it feels a lot more like Rust in
    # an un-ergonomic way.
    var robot = Robot("Bob")
    var dragon = Dragon("Frank")
    introduction(robot)
    introduction(dragon)

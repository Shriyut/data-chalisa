package scalaBasics

object OopBasics {

  def main(args: Array[String]): Unit = {
    val person = new Person
    val animal = new Animal("goofy", 1)
    //name and age for animal class are class parameters not class members
    //class parameters are not fields
    //hence they cant be accessed by animal.name or animal.age in scala
    // to convert class parameter to class field add val keyword in the definition
    // class Animal(name: String, val age: Int)
    println(person)
    val animal1 = new AnimalNew("goofy", 1)
    println(animal1.age)
    animal1.greet("Arteezy")
    animal1.greet1()
  }


}

class Person
class Animal(name: String, age: Int) //constructor
class AnimalNew(name: String, val age: Int) {
  //implementation of the class
  //value of this code block will be ignored
  //at every instantiation of the class this particular block of code will be executed
  def greet(name: String): Unit = println(s"Welcome ${this.name}, from $name")
  //this.name will refer to the name parameter of class definition
  //overloading - methods with same name but different signatures
  def greet1(): Unit = println(s"Hi $name") //$name here is equivalent to this.name

  //overloading constructors
  def this(name: String) = this(name, 0) //d efualt value can be defined in the class definition itself
  def this() = this("John Doe") // only previously defined constructors can be referred
}

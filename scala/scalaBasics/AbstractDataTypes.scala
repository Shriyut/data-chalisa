package scalaBasics

object AbstractDataTypes {
  def main(args: Array[String]): Unit = {
    val dog = new Dog
    val croc = new Crocodile
    croc.eat(dog)
  }
  abstract class Animal{
    //abstract classes can have abstract and non abstract data types
    //val creatureType: String
    val creatureType: String = "wild"
    def eat: Unit
    //sub classes will contain the implementation/values for these
    //abstract classes cannot be instantiated
  }

  class Dog extends Animal{
    override val creatureType: String = "German Shepherd"

    def eat: Unit = println("crunch")
    //override keyword is not mandatory for abstract members
    //override is required when method or parameter is not abstract i.e. has an implementation
    }

  //Traits
  trait Carnivore {
    def eat(animal: Animal): Unit
    //no implementation like abstract classes
    //unlike abstract classes traits  can be inherited along classes
    //traits donot have constructor parameters
    //traits are implemented to replicate a type of behaviour
  }

  class Crocodile extends Animal with Carnivore {
    //multiple traits can be inherited by the same class
    override val creatureType: String = "Logia"

    override def eat: Unit = println("chop")

    override def eat(animal: Animal): Unit = println(s"I eat ${animal.creatureType}")
  }

  //scala.AnyRef is equivalent to java.lang.Object
  //scala.Any is the parent type of all scala objects
  //scala.null - Null reference
  //scala.AnyVal contains primitive data types
  //scala.Nothing - sub type of every type in scala
  //method definition can be supplied ??? to add logic later so that the code doesnt result in error
  //def head: Int = ???
}

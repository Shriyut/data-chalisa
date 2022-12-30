package scala

object Inheritance {

  def main(args: Array[String]): Unit = {
    cat.eat

    val dog = new Dog
    dog.eat
  }

  class Animal {
    def eat = println("zzzz")
  }

  //scala offers single class inheritance
  class Cat extends Animal

  val cat = new Cat

  class Person(name: String, age: Int) {

  }

  class Adult(name: String, age: Int, id: String) extends Person(name, age)
  //constructor of parent class is called first in JVM

  //overriding
  class Dog extends Animal {
    override def eat  = {
      super.eat
      println("crunch")
    }
  }
  //super is used when you want to reference a method or parameter froom parent class

  //preventing overriding
  //final keyword (can be used on the class itself)
  //another option can be to seal the class using the keyword sealed, can be extended in the same file but not in other files
}

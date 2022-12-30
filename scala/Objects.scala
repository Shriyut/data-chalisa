package scala

object Objects {

  //scala does not have class level functionality i.e. it has no concept of static
  //objects are used to have static like functionality
  object Person { //type (Person) + its only instance
    //static/class level functionality
    val N_EYES = 2
    //this is equivalent to public static final int N_EYES = 2 in scala
    def canFly: Boolean = false

    //scala objects are used as singleton instances

    //factory method
    def from(mother: Person, father: Person): Person = new Person("Fred")
    //this can be named as apply


  }

  class Person(name: String){
    //instance-level functionality
    // this is to separate instance level functionality from static/class level functionality
    //this pattern is known as companions

  }

  def main(args: Array[String]): Unit = {
    println(Person.N_EYES)
    println(Person.canFly)

    val sunny = Person
    val shanu = Person
    println(sunny == shanu) //returns true

    val mary = new Person("Mary")
    val john = new Person("John")
    println(mary == john) //returns false

    val fred = Person.from(mary, john)

    //scala applications - scala object with main method i.e. the current block
    //scala application is a scala object with main method implemented
  }
}

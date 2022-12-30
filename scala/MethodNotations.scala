package scala

import scala.language.postfixOps //imported for syntactical sugar of postfix annotation

object MethodNotations {
  def main(args: Array[String]): Unit = {
    val mary = new Person("Mary", "Inception")
    println(mary.likes("Inception"))
    println( mary likes "Inception") //infix notation = operator notation, only works with methods that have one parameter
    //infix notations are examples of syntactic sugar
    val sunny = new Person("Sunny", "FightClub")
    println(mary hangOut sunny)
    // all operators are methods in scala

    //prefix notation - another form syntactic sugar
    val x = -1 //equivalent with 1.unary_-1
    //unary_prefix only works with these operators - + ~ !
    println(!mary)
    println(mary.unary_!) //equivalent

    //postfix notation
    println(mary.isAlive)
    println(mary isAlive) //equivalent

    //apply
    println(mary.apply())
    println(mary()) //equivalent
    //whenever the compiler sees the object being called like a function it looks for definition of apply in the class

    println((+mary).age)
    println(sunny learnsScala)
    println(mary(10))
  }
  class Person(val name: String, favMovie: String,val age: Int = 0){
    def likes(movie: String): Boolean = movie == favMovie
    def hangOut(person: Person): String = s"${this.name} hangs out with ${person.name}"
    //space between ! and : is important here
    def unary_! : String = s"$name, what the heck?!"
    def unary_+ : Person = new Person(name, favMovie, age+1)
    def isAlive: Boolean = true
    def apply(): String = s"$name likes $favMovie"
    def apply(n: Int): String = s"$name has watched $favMovie $n times"
    def learns(thing: String) = s"$name is learning $thing"
    def learnsScala = this learns "Scala"
  }



}

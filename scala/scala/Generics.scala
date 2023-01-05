package scala

object Generics {

  def main(args: Array[String]): Unit = {
    val list = new MyList[Int]
    val emptyListOfIntegers = MyList.empty[Int]
  }

  //similar approach is applicable to traits as well
  //trait MyMap[K,V]
  class MyList[T] {
    //generic value T
  }
  class MyMap[K, V]

  //generic methods
  object MyList {
    //objects cannot be type parameterized
    def empty[T]: MyList[T] = ???
  }

  //variance problem

  class Animal
  class Cat extends Animal
  class Dog extends Animal

  //list[Cat] extends list[Animal] - covariance
  //+ sign denotes the class to be covariant
  class CovariantList[+T]
  val animal: Animal = new Cat
  val animalList: CovariantList[Animal] = new CovariantList[Cat]
  //object type of Dog can be added to the list which could theoretically pollute the contents of the list

  //invariance
  class InvariantList[T]
  //val invariantAnimalL: InvariantList[Animal] = new InvariantList[Cat] - results in error
  val invariantAnimalL: InvariantList[Animal] = new InvariantList[Animal]

  //contravariance
  class ContraVariantList[-T]
  val contraVariantList: ContraVariantList[Cat] = new ContraVariantList[Animal]

  //BoundedTypes

  //BoundedTypes allow the generic classes to be used only for certain types that are
  // either a sub class of a different type or a super class of a different type

  //upper bound type
  class Cage[T <: Animal](animal: T) //only accepts parameter that are subtype of Animal
  val cage = new Cage(new Dog)

//  class Car
//  val newCage = new Cage(new Car) - will throw error at runtime

  //lower bound type
  class Prison[T >: Animal](animal: T) //only accepts supertype of class Animal 
}

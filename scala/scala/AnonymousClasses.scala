package scala

object AnonymousClasses {

  def main(args: Array[String]): Unit = {
    println(animal.getClass)
  }

  trait Animal {
    def eat: Unit
  }

  //AnonymousClass
  val animal: Animal = new Animal {
    override def eat: Unit = println("haha")
  }


}

package scala

object CaseClasses {

  def main(args: Array[String]): Unit = {
    val jim = new Person("Jim", 14)
    println(jim.name)
    println(jim.toString)
  }

  case class Person(name: String, age: Int){
    //cae classes promote all parameters to field
    //equals and hashCode are implemented out of the box in case classes
    //in built copy method including overriding parameters
    //case classes are serializable
    //case classes have extractor patterns i.e. can be used in pattern matching
  }
}

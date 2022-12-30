package scala.FunctionalProgramming

object Options {

  def main(args: Array[String]): Unit = {
    //Option is a wrapper for a value that might be present or not
    val myFirstOption: Option[Int] = Some(4)
    val noOption: Option[Int] = None

    println(myFirstOption)
    //options were invented to deal with unsafe apis (no need to perform null checks)
    def unSafeMethod(): String = null
    

  }

}

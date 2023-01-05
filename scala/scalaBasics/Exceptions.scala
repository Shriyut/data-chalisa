package scalaBasics

object Exceptions {

  def main(args: Array[String]): Unit = {
    val x: String = null
    //println(x.length) //throws null pointer exception
    // throw new NullPointerException - this is treated as an expression in scala
    //exceptions are instances of classes

    //throwable classes extend the throwable class
    //Exception and Error are major Throwable subtypes

    //Exceptions are JVM specific
    try{
      getInt(true)
    }catch {
      case e: RuntimeException => println("Caught RuntimeException")
      //case e: RintimeException => 43
    }finally{
      println("Finally block")
    }
  }

  def getInt(withExceptions: Boolean): Int =
    if(withExceptions) throw new RuntimeException("Not for you")
    else 49

  //defining custom exceptions

  class MyException extends Exception
  val exception = new MyException
  //throw Exception
}

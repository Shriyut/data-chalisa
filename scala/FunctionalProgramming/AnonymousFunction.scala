package scala.FunctionalProgramming

object AnonymousFunction {

  def main(args: Array[String]): Unit = {
    //Object oriented way of defining a function
    val doubler = new Function1[Int, Int] {
      override def apply(x: Int) = x * 2
    }

    //Anonymous function (lambda)
    val doubler2 = (x: Int) => x * 2
    //val doubler: Int => Int = x => x * 2 //similar to above

    //multiple parameters in lambda
    val adder: (Int, Int) => Int = (a: Int, b: Int) => a+b

    //no parameters
    val doSomething: () => Int = () => 3

    //lambdas must be called with parenthesis
    println(doSomething())

    //curly braces with lambda
    val stringToInt = {
      (str: String) => str.toInt
    }

    //more syntactical sugar
    val niceIncrementer: Int => Int = _ + 1
    //above line is equivalent to
    // val niceIncrementer: Int => Int = (x: Int) => x + 1
    val niceAdder: (Int, Int) => Int = _ + _ //equivalent to (a, b) => a + b
    //each underscore stands for a different parameter
    
  }

}

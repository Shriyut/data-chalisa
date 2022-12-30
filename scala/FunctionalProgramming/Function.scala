package scala.FunctionalProgramming

object Function {

  def main(args: Array[String]): Unit = {
    val doubler = new MyFunction[Int, Int] {
      override def apply(element: Int): Int = element*2
    }

    println(doubler(2))
    //scala supports such function types upto 22 parameters

    //function types with 2 input and 1 result parameter
    //Function2[A, B, R]
    //can be denoted as (A, B) => R

    val adder: ((Int, Int) => Int) = new Function2[Int, Int, Int] {
      override def apply(a: Int, b:Int): Int = a + b
    }
    println(adder(1, 2))

    //all scala functions are objects

    //higher order functions - either receive functions as parameter or return other functions as result
    //Function1[Int, Function1[Int, Int]]
    val higherOrderFunction: Function1[Int, Function1[Int, Int]] = new Function1[Int, Function1[Int, Int]] {
      override def apply(x: Int): Function1[Int, Int] = new Function1[Int, Int] {
        override def apply(y: Int): Int = x + y
      }
    }

    println(higherOrderFunction(3)(7)) //curried function

  }

  trait MyFunction[A, B] {
    def apply(element: A): B
  }


}

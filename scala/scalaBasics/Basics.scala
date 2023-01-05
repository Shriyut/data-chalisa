package scalaBasics

object Basics {

  def main(args: Array[String]): Unit = {
    //Unit == void in scala
    println("lessgo!!")

    //vals are immutable in scala (not intended to be used as constants) - no need to specify the type, compiler can infer types
    val x: Int = 42
    val longValue = 42L
    val floatValue = 2.0f
    val doubleVlaue = 3.14

    //variables
    var a = 4
    //variables can be reassigned but values cannot be reassigned
    //changing a variable is known as side effect

    val v = 1 + 2 //expression
    // +- * / & ! << >> >>> (right shift with zero extension) == != > < >= <= && || {+= -= *= /=} side effect operators

    //everything in scala is an expression(except definitions)
    val con = true
    val check = if(con) 4 else 5
    println(check)

    //its preferred to not use loops in scala since its not an imperative programming language
    //instructions are executed (in java), expressions are evaluated (scala)

    val weird = ( a = 3)
    //reassigning a variable is side effect, side effects in scala are expressions returning a unit
    //side effect examples - println(), whiles, reassigning variables
    println(weird)

    //Code Blocks
    // value of the block is the value of its last expression
    val codeBlock = {
      val y = 2
      val z = 3

      if( z > y) "hello" else "world"
      //42 if uncommented the value of the block becomes 42
    }

    def func(a: String, b:Int): String = {
      a + " " + b
    }

    //when loops are needed it is advised to use recursion instead
    //compiler cant figure out the return type of recursive function on its own
    def repeat(a: String, b: Int): String = {
      if( b == 1) a
      else a + repeat(a, b-1)
    }

    //its better to use tail recursion ( use recursive call as the last expression)
    // or the annotaion @tailrec can be used, if the function is not tail recursive compiler will throw an error
    //when loops are needed tail recursion can be used
    // repeat (x, x-1) is tail recursive but a + repeat(a, b-1) is not tail recursive

    def callByValue(x: Long): Unit = {
      println("By Value : "+ x)
      println("By Value : "+ x)
    }

    def callByName(x: => Long): Unit = {
      println("By Name : "+ x)
      println("By Name : "+ x)
    }

    callByValue(System.nanoTime()) // expression passed as value (constant)
    callByName(System.nanoTime())  // expression is evaluated each time
    // => delays the evaluation of expression passed as parameter



  }

}

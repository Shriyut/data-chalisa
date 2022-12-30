package scala.FunctionalProgramming

object MapAndFilter {

  def main(args: Array[String]): Unit = {

  }

  val list = List(1,2,3)
  println(list.head)
  println(list.tail)

  //map
  println(list.map(_ + 1))
  println(list.map(_ + "is a number"))

  //filter
  println(list.filter(_ % 2 == 0))
  // _ denotes all elements of the list

  //flatMap
  val toPair = (x: Int) => List(x, x+1)
  println(list.flatMap(toPair))

  //iterations
  val numbers = List(1,2,3,4)
  val chars = List('a', 'b', 'c', 'd', 'e')
  val combinations = numbers.flatMap(n => chars.map(c => "" + c + n))
  println(combinations)

  //foreach
  list.foreach(println)

  val colors = List("Blue", "Green")
  //for comprehensions
  val forCombinations = for {
    n <- numbers // if n %2 == 0 // filter condition
    c <- chars
    color <- colors
  } yield "" + c + n + "-" + color
  println(forCombinations)

  //syntax overload
  list.map { x =>
    x * 2
  }
}

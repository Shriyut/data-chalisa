package scala.FunctionalProgramming

object Sequences {
  //Collections in scala are of two types mutable and immutable
  //TODO: Understand the hierarchy of collections thoroughly (time complexities etc)
  def main(args: Array[String]): Unit = {
    //Sequences are a general interface for data structures that have a well defined order and can be indexed
    val aSeq = Seq(1,2,3,4)
    println(aSeq)
    println(aSeq.reverse)
    println(aSeq(2)) // equivalent to get
    println(aSeq ++ Seq(5,6,7))
    println(aSeq.sorted)

    //Ranges
    val aRange: Seq[Int] = 1 to 10
    aRange.foreach(println)

    (1 to 10).foreach(x => println("Hello"))

    //lists
    val aList = List(1,2,3)
    val prepend = 42 +: aList :+ 89
    println(prepend)

    //vectors
    val vecotr: Vector[Int] = Vector(1,2,3)
    println(vecotr)

    //tuples - finite ordered "lists"
    val aTuple = new Tuple2(2, "Hello") // upto 22 parameter size
    println(aTuple._1)
    println(aTuple.copy(_2 = "goodbye"))
    println(aTuple.swap)

    //Maps
    val aMap: Map[String, Int] = Map()
    val phoneBook = Map(("Jim", 555), "Dan"-> 789).withDefaultValue(-1)
    println(phoneBook)

    //add a pairing
    val newPairing = "Mary" -> 5678
    val newPhoneBook = phoneBook + newPairing

    println(phoneBook.map(pair => pair._1.toLowerCase -> pair._2))

    val names = List("Bob", "James", "Mary", "Jane", "Jose")
    println(names.groupBy(name => name.charAt(0)))

  }

}

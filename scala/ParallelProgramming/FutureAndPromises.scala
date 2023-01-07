package ParallelProgramming

import scala.concurrent.Future
//important for futures
import scala.concurrent.ExecutionContext.Implicits.global
import scala.util.Success
import scala.util.Failure

object FutureAndPromises {

  def main(args: Array[String]): Unit = {
    def meaningOfLife: Int = {
      Thread.sleep(2000)
      42
    }

    val aFuture = Future {
      meaningOfLife
    } // (global) which is passed by compiler

    println(aFuture.value) //will return an option - Option[Try[Int]] Int since this future will hold an Int value
    //option is returned because the future might have failed or it might not have finished at that time

    //waiting on the future
    aFuture.onComplete(t => t match {
      case Success(meaningOfLife) => println(s"Found meaning of life $meaningOfLife")
      case Failure(e) => println(s"There is no meaning in life $e")
    }) // will be called by some thread

    Thread.sleep(3000)//applying sleep so that main JVM thread keeps on running until the callback on future is complete
  }

}

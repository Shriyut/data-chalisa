package ParallelProgramming

import java.util.concurrent.Executors

object Concurrency {

  def main(args: Array[String]): Unit = {
    val threadHello = new Thread(() => (1 to 5).foreach(_ => println("Hello")))
    val threadGoodBye = new Thread(() => (1 to 5).foreach(_ => println("GoodBye")))
    threadHello.start()
    threadGoodBye.start()

    //executors
    val pool = Executors.newFixedThreadPool(10)
    pool.execute(() => println("Something in the thread pool"))

    pool.execute(() => {
      Thread.sleep(1000)
      println("Done after 1 second")
    })

    pool.execute(() => {
      Thread.sleep(1000)
      println("Almost Done")
      Thread.sleep(1000)
      println("Done after 2 seconds")
    })

    pool.shutdown()

    //race condition

    case class BankAccount(var amount: Int)

    def buy(bankAccount: BankAccount, thing: String, price: Int): Unit = {
      //multiple threads can access the code below
      bankAccount.amount -= price
    }

    def buySafe(bankAccount: BankAccount, thing: String, price: Int): Unit = {
      bankAccount.synchronized {
        //synchronized doesnt allow threads to run the critical section(code defined in synchronized block) at the same
        // time
        bankAccount.amount -= price
      }
    }

    def demoBankingProblem(): Unit = {
      (1 to 10000).foreach {
        _ =>
          val account = new BankAccount(50000)
          val thread1 = new Thread(() => buy(account, "stuff", 4000))
          val thread2 = new Thread(() => buy(account, "gadgets", 5000))
          thread1.start()
          thread2.start()
          thread1.join()
          thread2.join()
          if( account.amount != 41000) println(s"Bank scammed: Current Balance ${account.amount}")
      }
    }

    demoBankingProblem()
  }

}

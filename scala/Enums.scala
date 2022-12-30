package scala

object Enums {

  def main(args: Array[String]): Unit = {
    val somePermissions: Permissions = Permissions.READ
    somePermissions.openDocument()

    val somePermissionOrdinal = somePermissions.ordinal
    val allPermissions = Permissions.values //displays all values of the enum
    val readPermission = Permissions.valueOf("READ") //enums can be referenced from string
  }

  enum Permissions {
    case READ, WRITE, EXECUTE, NONE

    //add fields/methods
    def openDocument(): Unit =
      if(this == READ) println("Opening Document")
      else println("Acces Denied")
  }

  //Enums can also take constructor arguments
  enum PermissionsWithBits(bits: Int) {
    case READ extends PermissionsWithBits(4)
  }

  //companiion objects for enums can be used as source for factory methods
  object PermissionsWithBits {
    def fromBits(bits: Int): PermissionsWithBits = PermissionsWithBits.READ
  }

}

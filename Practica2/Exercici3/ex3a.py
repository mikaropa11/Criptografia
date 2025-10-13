def parseHexToDec(hex):
    hex = hex.replace("\n", "").replace(" ", "").replace(":", "")
    decimal = int(hex, 16)
    print("El numero decimal")
    print(decimal)

hex = input("Entra el numero hexadecimal:\n")
parseHexToDec(hex)
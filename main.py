from scripts.check_area import consulta



def main():
    running = True
    while running:
        print("-----------------")
        print("  CEP-GEOFINDER ")
        print("------------------")
        latitude = float(input("Enter Latitude (Ex: -23.5489): "))
        longitude = float(input("Enter Longitude (Ex: -46.6388): "))
        radius = float(input("Enter Radius(Km): "))
        result = consulta(latitude, longitude, radius)
        count = 0
        for i in result:
            count += 1
            print(i)
        print(f"{count} CEPs were found in that radius\n")
        input("Press any key to continue...")

if __name__ == "__main__":
    main()
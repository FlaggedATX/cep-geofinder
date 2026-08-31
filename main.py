from scripts.check_area import consulta



def main():
    running = True
    while running:
        print("-----------------")
        print("  CEP-GEOFINDER ")
        print("------------------")
        latitude = float(input("Enter Latitude: "))
        longitude = float(input("Enter Longitude: "))
        radius = float(input("Enter Radius: "))
        result = consulta(latitude, longitude, radius)
        count = 0
        for i in result:
            count += 1
            print(i)
        print(f"{count} CEPs were found in that radius\n")

if __name__ == "__main__":
    main()
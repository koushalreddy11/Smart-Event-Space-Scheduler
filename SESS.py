import json

events = []
rooms = []
bookings = []

# -------------------- EVENT --------------------
def add_event():
    title = input("Enter Event Title: ")
    date = input("Enter Date (YYYY-MM-DD): ")
    start = int(input("Start Time (24hr): "))
    end = int(input("End Time (24hr): "))
    dept = input("Department: ")

    if start >= end:
        print("Invalid time range")
        return

    event = {
        "id": len(events) + 1,
        "title": title,
        "date": date,
        "start": start,
        "end": end,
        "dept": dept
    }

    events.append(event)
    print("Event Added")


def view_events():
    if not events:
        print("No events found")
        return

    for e in events:
        print(e)


# -------------------- ROOM --------------------
def add_room():
    rid = input("Enter Room ID: ")
    capacity = int(input("Capacity: "))
    features = input("Features (comma separated): ").split(",")

    room = {
        "id": rid,
        "capacity": capacity,
        "features": features
    }

    rooms.append(room)
    print("Room Added")


def view_rooms():
    if not rooms:
        print("No rooms found")
        return

    for r in rooms:
        print(r)


# -------------------- BOOKING --------------------
def book_room():
    if not events or not rooms:
        print("Add events and rooms first")
        return

    view_events()
    eid = int(input("Select Event ID: "))

    view_rooms()
    rid = input("Select Room ID: ")

    event = next((e for e in events if e["id"] == eid), None)
    room = next((r for r in rooms if r["id"] == rid), None)

    if not event or not room:
        print("Invalid selection")
        return

    # Check conflict
    for b in bookings:
        if b["room"] == rid and b["date"] == event["date"]:
            if event["start"] < b["end"] and event["end"] > b["start"]:
                print("Time conflict")
                return

    booking = {
        "event": event["title"],
        "room": rid,
        "date": event["date"],
        "start": event["start"],
        "end": event["end"]
    }

    bookings.append(booking)
    print("Booking Confirmed")


# -------------------- AVAILABILITY --------------------
def check_availability():
    date = input("Enter Date (YYYY-MM-DD): ")
    time = int(input("Enter Time (24hr): "))

    if not rooms:
        print("No rooms available")
        return

    for r in rooms:
        available = True

        for b in bookings:
            if b["room"] == r["id"] and b["date"] == date:
                if time >= b["start"] and time < b["end"]:
                    available = False
                    break

        if available:
            print("Available:", r["id"])
        else:
            print("Occupied:", r["id"])


# -------------------- REPORT --------------------
def generate_report():
    print("\nREPORT")
    print("Total Events:", len(events))
    print("Total Rooms:", len(rooms))
    print("Total Bookings:", len(bookings))


# -------------------- CHART --------------------
def show_charts():
    try:
        import matplotlib.pyplot as plt

        room_usage = {}
        for b in bookings:
            room_usage[b["room"]] = room_usage.get(b["room"], 0) + 1

        if not room_usage:
            print("No booking data to display")
            return

        plt.bar(room_usage.keys(), room_usage.values())
        plt.title("Room Usage")
        plt.xlabel("Rooms")
        plt.ylabel("Bookings")
        plt.show()

    except:
        print("Matplotlib not installed")


# -------------------- FILE SAVE --------------------
def save_data():
    with open("data.json", "w") as f:
        json.dump({
            "events": events,
            "rooms": rooms,
            "bookings": bookings
        }, f)


def load_data():
    global events, rooms, bookings
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            events = data.get("events", [])
            rooms = data.get("rooms", [])
            bookings = data.get("bookings", [])
    except:
        pass


# -------------------- MAIN MENU --------------------
def main():
    load_data()

    while True:
        print("\n===== SESS MENU =====")
        print("1. Add Event")
        print("2. View Events")
        print("3. Add Room")
        print("4. Book Room")
        print("5. Check Availability")
        print("6. Generate Report")
        print("7. Show Charts")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_event()
        elif choice == '2':
            view_events()
        elif choice == '3':
            add_room()
        elif choice == '4':
            book_room()
        elif choice == '5':
            check_availability()
        elif choice == '6':
            generate_report()
        elif choice == '7':
            show_charts()
        elif choice == '8':
            save_data()
            print("Exiting...")
            break
        else:
            print("Invalid choice")


# -------------------- RUN --------------------
if __name__ == "__main__":
    main()
# Hostel Room Allocation Management System
# Done by: Ajay

import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hostel_data.json")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    # default rooms: 101-105 with capacity 2, 201-203 with capacity 3
    rooms = {}
    for r in range(101, 106):
        rooms[str(r)] = {"capacity": 2, "students": []}
    for r in range(201, 204):
        rooms[str(r)] = {"capacity": 3, "students": []}
    return {"rooms": rooms}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_room(data):
    room_no = input("Enter new room number: ").strip()
    if room_no in data["rooms"]:
        print("Room already exists.")
        return
    try:
        capacity = int(input("Enter room capacity: "))
    except ValueError:
        print("Invalid capacity.")
        return
    data["rooms"][room_no] = {"capacity": capacity, "students": []}
    save_data(data)
    print(f"Room {room_no} added.")


def view_rooms(data):
    print("\n--- All Rooms ---")
    for room_no, room in data["rooms"].items():
        names = ", ".join(s["name"] for s in room["students"]) or "-"
        print(f"Room {room_no} | {len(room['students'])}/{room['capacity']} | Students: {names}")


def view_vacancies(data):
    print("\n--- Rooms with Vacancies ---")
    total = 0
    for room_no, room in data["rooms"].items():
        free = room["capacity"] - len(room["students"])
        if free > 0:
            print(f"Room {room_no}: {free} bed(s) free")
            total += free
    print(f"Total vacant beds: {total}")


def find_student(data, roll):
    for room_no, room in data["rooms"].items():
        for s in room["students"]:
            if s["roll"] == roll:
                return room_no, s
    return None, None


def allocate_room(data):
    roll = input("Enter student roll number: ").strip().upper()
    if find_student(data, roll)[0]:
        print("Student already has a room.")
        return
    name = input("Enter student name: ").strip().title()
    branch = input("Enter branch: ").strip().upper()
    room_no = input("Enter room number (or press Enter for auto allocation): ").strip()

    if not room_no:
        for r, room in data["rooms"].items():
            if len(room["students"]) < room["capacity"]:
                room_no = r
                break
        else:
            print("No vacant rooms available.")
            return

    room = data["rooms"].get(room_no)
    if room is None:
        print("Room does not exist.")
        return
    if len(room["students"]) >= room["capacity"]:
        print("Room is full.")
        return
    room["students"].append({"roll": roll, "name": name, "branch": branch})
    save_data(data)
    print(f"{name} allocated to room {room_no}.")


def vacate_room(data):
    roll = input("Enter student roll number: ").strip().upper()
    room_no, student = find_student(data, roll)
    if not room_no:
        print("Student not found.")
        return
    data["rooms"][room_no]["students"].remove(student)
    save_data(data)
    print(f"{student['name']} vacated room {room_no}.")


def search_student(data):
    roll = input("Enter student roll number: ").strip().upper()
    room_no, student = find_student(data, roll)
    if room_no:
        print(f"{student['name']} ({student['branch']}) is in room {room_no}.")
    else:
        print("Student not found.")


def main():
    data = load_data()
    while True:
        print("\n===== HOSTEL ROOM ALLOCATION MANAGEMENT =====")
        print("1. View all rooms")
        print("2. View vacancies")
        print("3. Add room")
        print("4. Allocate room to student")
        print("5. Vacate room")
        print("6. Search student")
        print("7. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_rooms(data)
        elif choice == "2":
            view_vacancies(data)
        elif choice == "3":
            add_room(data)
        elif choice == "4":
            allocate_room(data)
        elif choice == "5":
            vacate_room(data)
        elif choice == "6":
            search_student(data)
        elif choice == "7":
            print("Thank you!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()

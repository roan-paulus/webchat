from uuid import uuid4


class Chat:
    def __init__(self):
        self.rooms: list[object] = []

    def get_room(self) -> object | None:
        """Returns a room that is not full."""
        for room in self.rooms:
            if not room.is_full():
                return room

    def get_user(self, user_sid: str) -> int:
        """Return the indexes of the room with the user you want to find."""
        for room_i, room in enumerate(self.rooms):
            user_i = room.users.index(user_sid)
            if user_i != -1:
                return room_i, user_i

    def add_room(self, slots: int) -> None:
        """Add an empty chat room to chat rooms then return the room."""
        room = Room(slots)
        self.rooms.append(room)
        return room


class Room:
    def __init__(self, slots: int) -> None:
        self.id: str = str(uuid4())
        self.users: list[str] = []

        # One person does not need a room
        if slots < 2:
            raise ValueError("A minimum of two slots is required.")
        self.slots = slots

    def add_user(self, user: str) -> None:
        """Add a user to this room if there is room left."""
        if not self.is_full():
            self.users.append(user)

    def is_full(self):
        """Check if there is room left, pun intended."""
        return len(self.users) >= self.slots

    def __str__(self):
        return f"ChatRoom:{str(self.id)}"


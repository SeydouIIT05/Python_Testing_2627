from server import bookingConfirmationMessage


def test_confirmation_gives_number_of_places_booked():
    message = bookingConfirmationMessage(3, {"name": "Summer Cup"})

    assert message == "Great-booking complete! 3 places booked for Summer Cup."


def test_confirmation_uses_singular_for_one_place():
    message = bookingConfirmationMessage(1, {"name": "Summer Cup"})

    assert message == "Great-booking complete! 1 place booked for Summer Cup."

import json
from flask import Flask,render_template,request,redirect,flash,url_for

MAX_PLACES_PER_COMPETITION = 12


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def findClubByEmail(email, listOfClubs):
    return next((club for club in listOfClubs if club['email'] == email), None)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = findClubByEmail(request.form.get('email', ''), clubs)
    if club is None:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            'booking.html', club=foundClub, competition=foundCompetition,
            maxPlaces=maxPlacesBookable(foundClub, foundCompetition)
        )
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def hasEnoughPoints(club, placesRequired):
    return placesRequired <= int(club['points'])


def deductPoints(club, placesRequired):
    club['points'] = int(club['points']) - placesRequired


def placesBookedBy(club, competition):
    return competition.get('bookings', {}).get(club['name'], 0)


def isWithinBookingLimit(club, competition, placesRequired):
    alreadyBooked = placesBookedBy(club, competition)
    return alreadyBooked + placesRequired <= MAX_PLACES_PER_COMPETITION


def recordBooking(club, competition, placesRequired):
    bookings = competition.setdefault('bookings', {})
    bookings[club['name']] = bookings.get(club['name'], 0) + placesRequired


def hasEnoughPlaces(competition, placesRequired):
    return placesRequired <= int(competition['numberOfPlaces'])


def placesLeftMessage(competition):
    placesLeft = int(competition['numberOfPlaces'])
    if placesLeft == 0:
        return 'This competition is full.'
    return (
        'Not enough places left in this competition: '
        f'{placesLeft} available.'
    )


def maxPlacesBookable(club, competition):
    alreadyBooked = placesBookedBy(club, competition)
    return min(
        int(club['points']),
        MAX_PLACES_PER_COMPETITION - alreadyBooked,
        int(competition['numberOfPlaces']),
    )


def renderBookingError(message, club, competition):
    flash(message)
    return render_template(
        'booking.html', club=club, competition=competition,
        maxPlaces=maxPlacesBookable(club, competition)
    ), 400


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if not hasEnoughPlaces(competition, placesRequired):
        return renderBookingError(
            placesLeftMessage(competition), club, competition
        )
    if not hasEnoughPoints(club, placesRequired):
        return renderBookingError(
            'Not enough points to book that many places.', club, competition
        )
    if not isWithinBookingLimit(club, competition, placesRequired):
        return renderBookingError(
            f'You cannot book more than {MAX_PLACES_PER_COMPETITION} places '
            'per competition.', club, competition
        )
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    deductPoints(club, placesRequired)
    recordBooking(club, competition, placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
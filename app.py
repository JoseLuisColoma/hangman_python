from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Lista de palabras para el juego
words = ['python', 'flask', 'programacion', 'juego', 'ahorcado']


def get_random_word():
    return random.choice(words).upper()


def initialize_game():
    session['word'] = get_random_word()
    session['guessed_letters'] = []
    session['wrong_guesses'] = 0


@app.route('/')
def index():
    initialize_game()
    return redirect(url_for('game'))


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        letter = request.form.get('letter').upper()
        if letter not in session['guessed_letters']:
            session['guessed_letters'].append(letter)
            if letter not in session['word']:
                session['wrong_guesses'] += 1

    word_display = ''.join([letter if letter in session['guessed_letters'] else '_' for letter in session['word']])
    game_over = session['wrong_guesses'] >= 6
    win = '_' not in word_display

    return render_template('game.html', word_display=word_display, wrong_guesses=session['wrong_guesses'],
                           guessed_letters=session['guessed_letters'], game_over=game_over, win=win)


@app.route('/reset')
def reset():
    initialize_game()
    return redirect(url_for('game'))


if __name__ == '__main__':
    app.run(debug=True)
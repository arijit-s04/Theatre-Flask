import os
from theatre.forms import AdminLoginForm, ShowAddForm
import ffmpeg
from theatre import app
from theatre.models import Movie


def getVideoMetadata(video_path):
    vid = ffmpeg.probe(os.path.join(app.root_path, 'static', video_path))
    metadata = {}
    metadata['resolution'] = f"{vid['streams'][0]['width']} x {vid['streams'][0]['height']}"
    try:
        metadata['duration'] = secToHours(float(vid['streams'][0]['duration']))
    except:
        metadata['duration'] = secToHoursDur(vid['streams'][0]['tags']['DURATION'])
    metadata['frame_rate'] = calculateFrameRate(vid['streams'][0]['avg_frame_rate'])
    return metadata


def secToHours(time):
    hr = int(time // 3600)
    min = int(time/60 - 60*hr)
    if hr == 0 and min == 0:
        return f'{int(time)}sec'
    if hr == 0:
        return f'{min}min'
    return f'{hr}hr {min}min'

def secToHoursDur(duration):
    duration = duration.split(':')
    hr = int(duration[0])
    min = int(duration[1])
    sec = int(duration[2].split('.')[0])

    if min == 0 and hr == 0:
        return f'{sec}sec'
    if hr == 0:
        return f'{min}min'
    return f'{hr}hr {min}min'


def calculateFrameRate(frame_rate):
    a = float(frame_rate.split('/')[0])
    b = float(frame_rate.split('/')[1])
    return f'{(a/b):.2f}'


# def copySingleFile(parent, filename):
#     subprocess.Popen(['cp', '/home/don/Downloads/FTP/Wizarding world/Harry_Potter_and_the_Chamber_of_Secrets_2002.mkv', '/home/don/test.mkv'])


def saveForm(form:ShowAddForm):
    title = form.title.data
    path = os.path.join(app.root_path, 'static')
    video_file = os.path.join(title.casefold(), form.path.data.filename.casefold())
    poster_file = os.path.join(title.casefold(), form.poster_path.data.filename.casefold())

    if not os.path.exists(os.path.join(path, title.casefold())):
        os.mkdir(os.path.join(path, title.casefold()))
    movie = None
    try:
        form.path.data.save(os.path.join(path, video_file))
        form.poster_path.data.save(os.path.join(path, poster_file))
        description = form.description.data
        year = form.year.data
        category = form.category.data

        movie = Movie(title=title, year=year,\
            category=category, description=description,\
            path=video_file, poster_path=poster_file)
    except Exception as e:
        print(e)
    
    return movie


build_query = lambda x: Movie.title.like('%' + x + '%')

def retrieveKeyWords(query):
    lst = query.split(" ")
    lst = list(map(build_query, lst))
    return lst


def checkCredentials(form:AdminLoginForm):
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    if username == form.username.data and password == form.password.data:
        return (True, 'Login Successful!')
    if username != form.username.data:
        return (False, 'Invalid username!')
    return (False, 'Invalid Password!')
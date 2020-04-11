# Views, have all the routes of our web page

from flask import render_template, request
from application_files import app, db
from application_files.Model import Points
from sqlalchemy import and_

@app.route('/')
def index():
    allPoints = Points.query.all()
    return render_template('index.html', allPoints=allPoints)

'''
1. Insert: insert a point and return a unique KEY for the inserted object 
• Input:
• Point: the point to be inserted 
• Output:
• A unique KEY for the inserted point
'''
@app.route('/add', methods=["GET",'POST'])
def add():
    print(request.form)
    newTextForPoint = "({},{})".format(request.form['XpointInsert'], request.form['YpointInsert'])
    checkIfPointExist = (bool(Points.query.filter_by(text=newTextForPoint).first()))
    if (checkIfPointExist == False):
        # create new point
        newPointModel = Points(text=newTextForPoint, xCoord=request.form['XpointInsert'], yCoord=request.form['YpointInsert'])
        # adding new point to the data base
        db.session.add(newPointModel)
        db.session.commit()
        newID = newPointModel.id
        allPoints = Points.query.all()
        print('You insert a new point!')
        return render_template('index.html', allPoints=allPoints,submissionSuccessfulAdd=True, newID=newID)
    else:
        allPoints = Points.query.all()
        print('This Point already exist :)')
        return render_template('index.html', allPoints=allPoints, errorAdd=True)
'''
2. Remove: remove a point for a given KEY
• Input:
• KEY: the key of the point to be removed
• Output:
• No output is expected
'''
@app.route('/delete', methods=["GET",'POST'])
def delete():
    insertedKey = request.form['keyToDeletePoint']
    checkIfKeyExist = (bool(Points.query.filter_by(id=insertedKey).first()))
    submission_successful = True
    if(checkIfKeyExist == True) and (int(insertedKey) > 0):
        print(request.form)
        Points.query.filter_by(id=insertedKey).delete()
        db.session.commit()
        allPoints = Points.query.all()
        print('You deleted a point!')
        return render_template('index.html', allPoints=allPoints, submissionSuccessfulDelete=True)
    else:
        allPoints = Points.query.all()
        print('Not valid Key :)')
        return render_template('index.html', allPoints=allPoints, errorDelete=True)
'''
3. Search: search all points contained in a rectangle. 
• Input:
• The search rectangle 
• Output:
• List of keys of the points contained in the rectangle

r.x ≤ p.x ≤ r.x + r.width and r.y ≤ p.y ≤ r.y +r.height.
'''
@app.route('/search', methods=['GET','POST'])
def search():
    allPoints = Points.query.all()
    Xstart = int(request.form['XlowerUP'])
    Ystart = int(request.form['XlowerUP'])

    width = int(request.form['rectangleWidth'])
    height = int(request.form['rectangleHeight'])
    if width < 0 or height <0:
        allPoints = Points.query.all()
        print('Not valid width or height  :) try again')
        return render_template('index.html', allPoints=allPoints, badInputWidthOrHeight=True)
    boundWidth = Xstart + width
    boundHeight = Ystart + height
    listOfPointsInRectangle = Points.query.filter(and_(Points.xCoord >= Xstart, Points.xCoord <= boundWidth,
                                                       Points.yCoord >= Ystart, Points.yCoord <= boundHeight)).all()
    if not listOfPointsInRectangle:
        allPoints = Points.query.all()
        print('No point inside :)')
        return render_template('index.html', allPoints=allPoints, EmptySearch=True)
    else:
        print('points inside:')
        print(listOfPointsInRectangle)
        return render_template('index.html', allPoints=allPoints,
                               listOfPointsInRectangle=listOfPointsInRectangle,
                               submissionSuccessfulSearch=True, width=width, height=height, Xstart=Xstart, Ystart=Ystart)

'''
4. Get: get the point for a given KEY
• Input:
• KEY: the key of the point to get
• Output:
• The point for the given or NOT FOUND error if there is no point for the given key.
'''

@app.route('/get', methods=['GET','POST'])
def get():
    print(request.form)
    allPoints = Points.query.all()
    insertedKeyGet = request.form['KeyForPoint']
    checkIfKeyExist = (bool(Points.query.filter_by(id=insertedKeyGet).first()))
    if (checkIfKeyExist == True):
        CurrentPointToBeGiven = Points.query.filter_by(id=insertedKeyGet).first()
        pointCoord = CurrentPointToBeGiven.text
        print(("You Get {} from key {}").format(pointCoord, insertedKeyGet))
        return render_template('index.html', allPoints=allPoints,submissionSuccessfulGet=True, pointCoord=pointCoord)
    else:
        print('NOT FOUND, there is no point for the given key')
        return render_template('index.html', allPoints=allPoints,errorGet=True)

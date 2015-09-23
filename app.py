import json
from dateutil.parser import parse
from flask import Flask, session, render_template, request
from flask.json import jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__, static_url_path='', static_folder='client/dist')
app.secret_key = 'clydecletusvonmetus'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///school'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Relationship Tables
favorite_schools = db.Table("favorite_schools",
    db.Column("student_id", db.Integer, db.ForeignKey("students.id"), nullable=False),
    db.Column("school_id", db.Integer, db.ForeignKey("schools.id"), nullable=False),
    db.PrimaryKeyConstraint('student_id', 'school_id')
)

viewed_schools = db.Table("viewed_schools",
    db.Column("student_id", db.Integer, db.ForeignKey("students.id"), nullable=False),
    db.Column("school_id", db.Integer, db.ForeignKey("schools.id"), nullable=False),
    db.PrimaryKeyConstraint('student_id', 'school_id')
)

# Database models
class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2))
    major = db.Column(db.String(50))
    favorite_schools = db.relationship('School', secondary=favorite_schools,
        backref=db.backref('students_fav', lazy='dynamic'))
    viewed_schools = db.relationship('School', secondary=viewed_schools,
        backref=db.backref('students_viewed', lazy='dynamic'))

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.pw_hash = bcrypt.generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def is_valid_password(self, pw_attempt):
        return bcrypt.check_password_hash(self.pw_hash, pw_attempt)

    def get_id(self):
        try:
            return unicode(self.id)
        except:
            return flask.flash("No user found")

    # def is_authenticated(self):
    #     return self.authenticated

class School(db.Model):
    __tablename__ = "schools"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(50))
    state_abbrv = db.Column(db.CHAR(2))
    state = db.Column(db.String(30))
    region = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    website = db.Column(db.String(50))
    mascot = db.Column(db.String(50))
    is_public = db.Column(db.Boolean)
    is_private = db.Column(db.Boolean)
    is_hbcu = db.Column(db.Boolean)
    is_tribal = db.Column(db.Boolean)
    is_religious = db.Column(db.Boolean)
    religious_affiliation = db.Column(db.String(50))
    urbanization = db.Column(db.String(10))
    urbanization_degree = db.Column(db.String(20))
    enrollment = db.Column(db.Integer)
    enrollment_range = db.Column(db.String(20))
    in_state_tuition = db.Column(db.Integer)
    out_state_tuition = db.Column(db.Integer)
    percent_admit = db.Column(db.Integer)
    percent_admit_men = db.Column(db.Integer)
    percent_admit_women = db.Column(db.Integer)
    graduate_enrollment = db.Column(db.Integer)
    undergrad_enrollment = db.Column(db.Integer)
    percent_amerindian_aknative = db.Column(db.Integer)
    percent_asian_nativehi_pacislander = db.Column(db.Integer)
    percent_asian = db.Column(db.Integer)
    percent_nativehi_pacislander = db.Column(db.Integer)
    percent_aficanamer = db.Column(db.Integer)
    percent_hispanic_latino = db.Column(db.Integer)
    percent_white = db.Column(db.Integer)
    percent_women = db.Column(db.Integer)
    percent_amerindian_aknative_undergrad = db.Column(db.Integer)
    percent_asian_nativehi_pacislander_undergrad = db.Column(db.Integer)
    percent_asian_undergrad = db.Column(db.Integer)
    percent_nativehi_pacislander_undergrad = db.Column(db.Integer)
    percent_aficanamer_undergrad = db.Column(db.Integer)
    percent_hispanic_latino_undergrad = db.Column(db.Integer)
    percent_white_undergrad = db.Column(db.Integer)
    percent_women_undergrad = db.Column(db.Integer)
    percent_amerindian_aknative_grad = db.Column(db.Integer)
    percent_asian_nativehi_pacislander_grad = db.Column(db.Integer)
    percent_asian_grad = db.Column(db.Integer)
    percent_nativehi_pacislander_grad = db.Column(db.Integer)
    percent_aficanamer_grad = db.Column(db.Integer)
    percent_hispanic_latino_grad = db.Column(db.Integer)
    percent_white_grad = db.Column(db.Integer)
    percent_women_grad = db.Column(db.Integer)
    act_75th_percentile = db.Column(db.Integer)
    act_25th_percentile = db.Column(db.Integer)
    sat_writing_75th_percentile = db.Column(db.Integer)
    sat_writing_25th_percentile = db.Column(db.Integer)
    sat_math_75th_percentile = db.Column(db.Integer)
    sat_math_25th_percentile = db.Column(db.Integer)
    sat_cr_75th_percentile = db.Column(db.Integer)
    sat_cr_25th_percentile = db.Column(db.Integer)
    ipeds_id = db.Column(db.CHAR(6))

db.create_all()
db.session.commit()

@login_manager.user_loader
def load_student(user_id):
    return Student.get(user_id)

# @app.before_request
# def load_user():
#     if session["user_id"] != None:
#         user = Student.query.filter_by(username=session["user_id"]).first()
#     else:
#         user = {"name": "Guest"}  # Make it better, use an anonymous User instead

#     g.user = user

# Serialize
class JsonSerializer(object):
    """A serializer that provides methods to serialize and deserialize JSON 
    dictionaries.

    Note, one of the assumptions this serializer makes is that all objects that
    it is used to deserialize have a constructor that can take all of the
    attribute arguments. I.e. If you have an object with 3 attributes, the
    constructor needs to take those three attributes as keyword arguments.
    """

    __attributes__ = None
    """The attributes to be serialized by the seralizer.
    The implementor needs to provide these."""

    __required__ = None
    """The attributes that are required when deserializing.
    The implementor needs to provide these."""

    __attribute_serializer__ = None
    """The serializer to use for a specified attribute. If an attribute is not
    included here, no special serializer will be user.
    The implementor needs to provide these."""

    __object_class__ = None
    """The class that the deserializer should generate.
    The implementor needs to provide these."""

    serializers = dict(
                        id=dict(
                            serialize=lambda x: uuid.UUID(bytes=x).hex,
                            deserialiez=lambda x: uuid.UUID(hex=x).bytes
                        ),
                        date=dict(
                            serialize=lambda x, tz: x.isoformat(),
                            deserialize=lambda x: dateutil.parser.parse(x)
                        )
                    )

    def deserialize(self, json, **kwargs):
        """Deserialize a JSON dictionary and return a populated object.

        This takes the JSON data, and deserializes it appropriately and then calls
        the constructor of the object to be created with all of the attributes.

        Args:
            json: The JSON dict with all of the data
            **kwargs: Optional values that can be used as defaults if they are not
                present in the JSON data
        Returns:
            The deserialized object.
        Raises:
            ValueError: If any of the required attributes are not present
        """
        d = dict()
        for attr in self.__attributes__:
            if attr in json:
                val = json[attr]
            elif attr in self.__required__:
                try:
                    val = kwargs[attr]
                except KeyError:
                    raise ValueError("{} must be set".format(attr))

            if(self.__attribute_serializer__ != None):
                serializer = self.__attribute_serializer__.get(attr)
            if serializer:               
                d[attr] = self.serializers[serializer]['deserialize'](val)
            else:
                d[attr] = val

        return self.__object_class__(**d)

    def serialize(self, obj):
        """Serialize an object to a dictionary.

        Take all of the attributes defined in self.__attributes__ and create
        a dictionary containing those values.

        Args:
            obj: The object to serialize
        Returns:
            A dictionary containing all of the serialized data from the object.
        """
        d = dict()
        for attr in self.__attributes__:
            val = getattr(obj, attr)
            if val is None:
                continue
            serializer = None
            if(self.__attribute_serializer__ != None):
                serializer = self.__attribute_serializer__.get(attr)
            if serializer:
                d[attr] = self.serializers[serializer]['serialize'](val)
            else:
                d[attr] = val

        return d

class SchoolJsonSerializer(JsonSerializer):
    __attributes__ = ['id','name','address','city','state_abbrv','state','region','latitude','longitude','website','mascot','is_public','is_private','is_hbcu','is_tribal','is_religious','religious_affiliation','urbanization','urbanization_degree','enrollment','enrollment_range','in_state_tuition','out_state_tuition','percent_admit','percent_admit_men','percent_admit_women','graduate_enrollment','undergrad_enrollment','percent_amerindian_aknative','percent_asian_nativehi_pacislander','percent_asian','percent_nativehi_pacislander','percent_aficanamer','percent_hispanic_latino','percent_white','percent_women','percent_amerindian_aknative_undergrad','percent_asian_nativehi_pacislander_undergrad','percent_asian_undergrad','percent_nativehi_pacislander_undergrad','percent_aficanamer_undergrad','percent_hispanic_latino_undergrad','percent_white_undergrad','percent_women_undergrad','percent_amerindian_aknative_grad','percent_asian_nativehi_pacislander_grad','percent_asian_grad','percent_nativehi_pacislander_grad','percent_aficanamer_grad','percent_hispanic_latino_grad','percent_white_grad','percent_women_grad','act_75th_percentile','act_25th_percentile','sat_writing_75th_percentile','sat_writing_25th_percentile','sat_math_75th_percentile','sat_math_25th_percentile','sat_cr_75th_percentile','sat_cr_25th_percentile','ipeds_id']
    __required__ = ['id']
    __attribute_serializer__ = None
    __object_class__ = School

# Routes
@app.route('/api/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us.
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.username.data).first_or_404()
        if user.is_valid_password(form.password.data):
            session['user_id'] = email
            login_user(user)
            flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/')

# Save e-mail to database and send to success page
@app.route('/api/student', methods=['POST'])
def create_student():
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    # Check that email does not already exist (not a great query, but works)
    # if not session.query(User).filter(User.email == email).count():
    new_user = Student(email, password, first_name, last_name)
    db.session.add(new_user)
    db.session.commit()
    return render_template('success.html')
    # return render_template('index.html')

@app.route('/api/student/school', methods=['POST'])
def add_viewed():
    school_name = request.json.get('school_name','')
    is_Favorite = request.json.get('is_Favorite','')
    user_id = session['user_id']
    school = School.query.filter_by(name=school_name).first_or_404()
    # user_id = 'test2@test2.com'
    student = Student.query.filter_by(email=user_id).first_or_404()
    message = None
    for item in student.viewed_schools:
        if item.id == school.id:
            message = "Viewed"
            break
        else:
            student.viewed_schools.append(school)
    if is_Favorite:
        for item in student.favorite_schools:
            if item.id == school.id:
                message = message + " Favorited"
                return message
            else:
                student.favorite_schools.append(school)
    db.session.commit()
    return "complete"

# School routes
@app.route('/api/school', methods=['GET'])
def get_schools():
    state = request.args.get('state')
    school_list = session.query(School).filter(School.state_abbrv == state).all()
    for x in school_list:
        print x.state
    return jsonify(json_list=SchoolJsonSerializer().serialize(school_list[0]))

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
@app.route('/')
@app.route('/register')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()

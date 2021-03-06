import json
import uuid
from dateutil.parser import parse
from flask import Flask, make_response, render_template, request, session
from flask.json import jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from flask.ext.bcrypt import Bcrypt
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Boolean, CHAR, Enum, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

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
    db.Column("school_id", db.Integer, db.ForeignKey("schools.id"), nullable=False)
)

viewed_schools = db.Table("viewed_schools",
    db.Column("student_id", db.Integer, db.ForeignKey("students.id"), nullable=False),
    db.Column("school_id", db.Integer, db.ForeignKey("schools.id"), nullable=False)
)

# Database models
class Student(db.Model, UserMixin):
    __tablename__ = "students"
    # id = db.Column(UUID(as_uuid=True), default=lambda: str(uuid.uuid4()), primary_key=True)
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(String(50), unique=True, nullable=False)
    pw_hash = db.Column(String(255), nullable=False)
    first_name = db.Column(String(50), nullable=False)
    last_name = db.Column(String(50), nullable=False)
    state = db.Column(Enum( 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', name='select_state'))
    major = db.Column(String(50))
    gender = db.Column(Enum('male', 'female', name='select_gender'))
    act = db.Column(Integer)
    sat_writing = db.Column(Integer)
    sat_math = db.Column(Integer)
    sat_cr = db.Column(Integer)
    urbanization = db.Column(Enum('city', 'rural', 'suburb', 'town', name='select_urban'))
    min_school_size = db.Column(Integer)
    max_school_size =db.Column(Integer)
    prefer_public = db.Column(Boolean, default=False)
    prefer_private = db.Column(Boolean, default=False)
    prefer_hbcu = db.Column(Boolean, default=False)
    prefer_tribal = db.Column(Boolean, default=False)
    prefer_religious = db.Column(Boolean, default=False)
    favorite_schools = relationship('School', secondary=favorite_schools,
        backref=backref('students_fav', lazy='dynamic'))
    viewed_schools = relationship('School', secondary=viewed_schools,
        backref=backref('students_viewed', lazy='dynamic'))

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.pw_hash = bcrypt.generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def is_valid_password(self, pw_attempt):
        return bcrypt.check_password_hash(self.pw_hash, pw_attempt)

    # def get_id(self):
    #     try:
    #         return unicode(self.id)
    #     except:
    #         return flask.flash("No user found")

    # def is_authenticated(self):
    #     return self.authenticated

class School(db.Model):
    __tablename__ = "schools"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(String(120))
    address = db.Column(String(120))
    city = db.Column(String(50))
    state_abbrv = db.Column(CHAR(2))
    state = db.Column(String(30))
    region = db.Column(String(50))
    latitude = db.Column(Float)
    longitude = db.Column(Float)
    website = db.Column(String(50))
    mascot = db.Column(String(50))
    is_public = db.Column(Boolean)
    is_private = db.Column(Boolean)
    is_hbcu = db.Column(Boolean)
    is_tribal = db.Column(Boolean)
    is_religious = db.Column(Boolean)
    religious_affiliation = db.Column(String(50))
    urbanization = db.Column(String(10))
    urbanization_degree = db.Column(String(20))
    enrollment = db.Column(Integer)
    enrollment_range = db.Column(String(20))
    in_state_tuition = db.Column(Integer)
    out_state_tuition = db.Column(Integer)
    percent_admit = db.Column(Integer)
    percent_admit_men = db.Column(Integer)
    percent_admit_women = db.Column(Integer)
    graduate_enrollment = db.Column(Integer)
    undergrad_enrollment = db.Column(Integer)
    percent_amerindian_aknative = db.Column(Integer)
    percent_asian_nativehi_pacislander = db.Column(Integer)
    percent_asian = db.Column(Integer)
    percent_nativehi_pacislander = db.Column(Integer)
    percent_aficanamer = db.Column(Integer)
    percent_hispanic_latino = db.Column(Integer)
    percent_white = db.Column(Integer)
    percent_women = db.Column(Integer)
    percent_amerindian_aknative_undergrad = db.Column(Integer)
    percent_asian_nativehi_pacislander_undergrad = db.Column(Integer)
    percent_asian_undergrad = db.Column(Integer)
    percent_nativehi_pacislander_undergrad = db.Column(Integer)
    percent_aficanamer_undergrad = db.Column(Integer)
    percent_hispanic_latino_undergrad = db.Column(Integer)
    percent_white_undergrad = db.Column(Integer)
    percent_women_undergrad = db.Column(Integer)
    percent_amerindian_aknative_grad = db.Column(Integer)
    percent_asian_nativehi_pacislander_grad = db.Column(Integer)
    percent_asian_grad = db.Column(Integer)
    percent_nativehi_pacislander_grad = db.Column(Integer)
    percent_aficanamer_grad = db.Column(Integer)
    percent_hispanic_latino_grad = db.Column(Integer)
    percent_white_grad = db.Column(Integer)
    percent_women_grad = db.Column(Integer)
    act_75th_percentile = db.Column(Integer)
    act_25th_percentile = db.Column(Integer)
    sat_writing_75th_percentile = db.Column(Integer)
    sat_writing_25th_percentile = db.Column(Integer)
    sat_math_75th_percentile = db.Column(Integer)
    sat_math_25th_percentile = db.Column(Integer)
    sat_cr_75th_percentile = db.Column(Integer)
    sat_cr_25th_percentile = db.Column(Integer)
    ipeds_id = db.Column(CHAR(6))

db.create_all()
db.session.commit()

@login_manager.user_loader
def load_student(user_id):
    return Student.query.get(user_id)

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
@app.route('/api/login', methods=['POST'])
def login():
    response = make_response()
    email = request.form['email']
    password = request.form['password']
    user = Student.query.filter_by(email=email).first_or_404()
    if user.is_valid_password(password):
        login_user(user, force=True)
        print('Logged in successfully.')
        print current_user.get_id()
        print current_user.is_authenticated()
        response.data = json.dumps({'data': True})
        # return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        response.data = json.dumps({'data': False})
    return response

@app.route('/api/logout')
# @login_required
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
# @login_required
def add_viewed():
    print current_user.is_authenticated()
    school_name = request.form['school_name']
    is_Favorite = request.form['is_Favorite']
    # user_id = current_user.get_id()
    school = School.query.filter_by(name=school_name).first_or_404()
    user_id = 'test1@test1.com'
    student = Student.query.filter_by(email=user_id).first_or_404()
    message = ""
    if len(student.viewed_schools) == 0:
        student.viewed_schools.append(school)
    else:
        for item in student.viewed_schools:
            if item.id == school.id:
                message = "Viewed"
                break
            else:
                student.viewed_schools.append(school)
    if is_Favorite:
        if len(student.favorite_schools) == 0:
            student.favorite_schools.append(school)
        else:
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
@app.route('/campus')
@app.route('/login')
@app.route('/register')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()

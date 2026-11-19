import sqlite3
from functools import wraps
from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "chennai-academy-secret-key-change-in-production"
DB_NAME = "academies.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first to continue.", "warning")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

init_db()

CATEGORY_IMAGES = {
    "Sports Academies": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=800&q=80",
    "Dance Academies": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80",
    "Music Academies": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=800&q=80",
    "Technology & Coding": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
    "Martial Arts Academies": "https://images.unsplash.com/photo-1555597673-b21d5c935865?auto=format&fit=crop&w=800&q=80",
    "Arts & Creative Skills": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=800&q=80",
    "Fitness & Wellness": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80",
    "Academic Coaching": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80",
    "Other Skill Development": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&q=80"
}

academies_data = {
    "Sports Academies": [
        {"name": "Trends Sports Academy", "category": "Badminton", "location": "Velachery", "phone": "7823900133", "email": "info@trendssports.com", "website": "https://trendssports.com", "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=800&q=80"},
        {"name": "SSS Multi Sports Hub", "category": "Badminton", "location": "Velachery", "phone": "6382412462", "email": "contact@sssmultisports.com", "website": "https://sssmultisports.com", "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=800&q=80"},
        {"name": "Dugout Sports", "category": "Cricket", "location": "Velachery", "phone": "9884212022", "email": "play@dugoutsports.in", "website": "https://dugoutsports.in", "image": "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=800&q=80"},
        {"name": "Head & Tail Turf & Sports Academy", "category": "Cricket", "location": "Ramapuram", "phone": "9176872003", "email": "support@headandtailturf.com", "website": "https://headandtailturf.com", "image": "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=800&q=80"},
        {"name": "Future Feathers Chess and Sports Academy", "category": "Chess", "location": "Ramapuram", "phone": "8438038064", "email": "chess@futurefeathers.com", "website": "https://futurefeathers.com", "image": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?auto=format&fit=crop&w=800&q=80"},
        {"name": "Abhinav Vijay Sports Academy", "category": "Badminton", "location": "Parangi Malai", "phone": "9677095551", "email": "kv@avsports.in", "website": "https://avsports.in", "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=800&q=80"},
        {"name": "Shree Sports Academy", "category": "Badminton", "location": "Kovilambakkam", "phone": "9940564616", "email": "shreesports@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=800&q=80"},
        {"name": "MTD SPORTS ACADEMY", "category": "Badminton", "location": "Pallikaranai", "phone": "9790760149", "email": "mtr@mtdsports.com", "website": "https://mtdsports.com", "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=800&q=80"},
        {"name": "Nutmeg", "category": "Futsal Court", "location": "Anna Nagar", "phone": "070107 31413", "email": "play@nutmegturf.com", "website": "https://nutmegturf.com", "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=800&q=80"},
        {"name": "GQUBE Sports Arena", "category": "Sport Complex", "location": "Kovilambakkam", "phone": "08925528298", "email": "arena@gqubesports.com", "website": "https://gqubesports.com", "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=800&q=80"},
        {"name": "Turf 137", "category": "Pickleball/Cricket/Football", "location": "Guindy", "phone": "08939737137", "email": "bookings@turf137.com", "website": "https://turf137.com", "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=800&q=80"},
        {"name": "Shazee Sports Arena", "category": "Badminton Court", "location": "Mambakkam", "phone": "09677046197", "email": "info@shazeesports.com", "website": "https://shazeesports.com", "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=800&q=80"},
        {"name": "Chaos Entertainment", "category": "Laser Tag Center", "location": "Adyar", "phone": "08148051055", "email": "fun@chaosent.in", "website": "https://chaosent.in", "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=800&q=80"},
        {"name": "FC MARINA TURF", "category": "Futsal Court", "location": "Thiruvanmiyur", "phone": "09962220400", "email": "info@fcmarinaturf.com", "website": "https://fcmarinaturf.com", "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=800&q=80"},
        {"name": "Takaro Turf", "category": "Sports Complex", "location": "Perungudi", "phone": "09894706999", "email": "play@takaroturf.com", "website": "https://takaroturf.com", "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=800&q=80"},
        {"name": "Smasher 3.0", "category": "Squash Court", "location": "Kottivakkam", "phone": "06374662761", "email": "squash@smasher3.com", "website": "https://smasher3.com", "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=800&q=80"}
    ],
    "Dance Academies": [
        {"name": "Airswings Dance Studio", "category": "Dance School", "location": "Thiruvanmiyur", "phone": "9884266105", "email": "dance@airswings.com", "website": "https://airswings.com", "image": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80"},
        {"name": "Leo's Dance Academy", "category": "Ballet School", "location": "Perungudi", "phone": "09840501105", "email": "leosdance@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1518834107812-67b0b7c58434?auto=format&fit=crop&w=800&q=80"},
        {"name": "Flying Feet Dance Studio", "category": "Dance School", "location": "Thiruvanmiyur", "phone": "08438104873", "email": "info@flyingfeet.in", "website": "https://flyingfeet.in", "image": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80"},
        {"name": "D'Alpha Dance Company", "category": "Hip Hop Dance", "location": "Adyar", "phone": "07305345789", "email": "alphadance@yahoo.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1547153760-18fc86324498?auto=format&fit=crop&w=800&q=80"},
        {"name": "Revel Dance Academy", "category": "Dance Company", "location": "Adyar", "phone": "09150007598", "email": "revel@danceademy.com", "website": "https://reveldance.com", "image": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80"},
        {"name": "Black Board Dance Academy", "category": "Dance Club", "location": "Velachery", "phone": "Not available", "email": "blackboarddance@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1547153760-18fc86324498?auto=format&fit=crop&w=800&q=80"},
        {"name": "Raack Academy of Dance Pallikaranai", "category": "Dance School", "location": "Pallikaranai", "phone": "9500078970", "email": "info@raackdance.com", "website": "https://raackdance.com", "image": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80"},
        {"name": "KSR Dance & Silambam Studio", "category": "Dance School", "location": "T. Nagar", "phone": "9840817454", "email": "ksrdance@silambam.org", "website": "https://ksrsilambam.com", "image": "https://images.unsplash.com/photo-1518834107812-67b0b7c58434?auto=format&fit=crop&w=800&q=80"}
    ],
    "Music Academies": [
        {"name": "MUZEOLA MUSIC ACADEMY", "category": "Vocals, Keyboard, Guitar, Violin, Veena, Flute", "location": "Velachery", "phone": "09942702708", "email": "muzeola@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=800&q=80"},
        {"name": "Creative Music Academy", "category": "Music School", "location": "Velachery", "phone": "Not available", "email": "creativemusic@yahoo.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?auto=format&fit=crop&w=800&q=80"},
        {"name": "Tansen Academy of Hindustani Vocal Music", "category": "Hindustani Vocal Music", "location": "Velachery", "phone": "09952993992", "email": "tansen@hindustanimusic.in", "website": "https://tansenacademy.in", "image": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?auto=format&fit=crop&w=800&q=80"},
        {"name": "Roys Music Academy", "category": "Intermediate Classes", "location": "Velachery", "phone": "09884630574", "email": "roysmusic@outlook.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=800&q=80"},
        {"name": "Dr TVG's Academy of Indian Music & Arts", "category": "Violin Classes", "location": "Velachery", "phone": "09566203821", "email": "drtvg@indianmusic.edu", "website": "https://drtvgmusic.org", "image": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?auto=format&fit=crop&w=800&q=80"},
        {"name": "Seven Notes Music School", "category": "Keyboard | Guitar | Piano | Violin", "location": "Madipakkam", "phone": "09445507749", "email": "sevennotes@musicschool.com", "website": "https://sevennotes.in", "image": "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?auto=format&fit=crop&w=800&q=80"},
        {"name": "Key 'n' Me", "category": "Music Theory", "location": "Velachery", "phone": "09840926795", "email": "keynme@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=800&q=80"},
        {"name": "Vidyarthi Centre of Excellence for Arts and Fine Arts", "category": "Carnatic Vocal | Keyboard | Bharatanatyam", "location": "Velachery", "phone": "08908909050", "email": "vidyarthi@artsedu.com", "website": "https://vidyarthiarts.com", "image": "https://images.unsplash.com/photo-1507838153414-b4b713384a76?auto=format&fit=crop&w=800&q=80"}
    ],
    "Technology & Coding": [
        {"name": "FITA Academy", "category": "Software Training Institute", "location": "Porur", "phone": "9345045466", "email": "support@fitaacademy.in", "website": "https://fitaacademy.in", "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80"},
        {"name": "Credo Systemz", "category": "Software Training Institute", "location": "Velachery", "phone": "9884412301", "email": "info@credosystemz.com", "website": "https://credosystemz.com", "image": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=800&q=80"},
        {"name": "Smart Skills Technologies", "category": "Training Center", "location": "Pallikaranai", "phone": "9043953743", "email": "smartskills@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80"},
        {"name": "Urbancode Training and Solutions", "category": "Software Training Institute", "location": "Pallikaranai", "phone": "9878798797", "email": "contact@urbancode.in", "website": "https://urbancode.in", "image": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=800&q=80"},
        {"name": "OrangeQuest Professional Training Academy", "category": "Education Center", "location": "Medavakkam", "phone": "9429692926", "email": "info@orangequest.com", "website": "https://orangequest.com", "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80"},
        {"name": "Velan Technologies", "category": "Software Training Institute", "location": "Perumbakkam", "phone": "9003777778", "email": "hr@velantech.com", "website": "https://velantech.com", "image": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=800&q=80"},
        {"name": "Karam Academy", "category": "Software Training Institute", "location": "Perumbakkam", "phone": "9894134423", "email": "info@karamacademy.com", "website": "https://karamacademy.com", "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80"},
        {"name": "Green Technology", "category": "Software Training Institute", "location": "Perumbakkam", "phone": "8939982138", "email": "green@greentech.com", "website": "https://greentechnology.in", "image": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=800&q=80"},
        {"name": "Aimore Technologies - Medavakkam", "category": "Software Training Institute", "location": "Medavakkam", "phone": "9728333334", "email": "info@aimoretechnologies.com", "website": "https://aimoretechnologies.com", "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80"},
        {"name": "AIITE - Best IT Training Academy in Chennai", "category": "Training Center", "location": "Medavakkam", "phone": "9884667742", "email": "aiite@softwaetraining.org", "website": "https://aiite.org", "image": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=800&q=80"}
    ],
    "Martial Arts Academies": [
        {"name": "Combat Kinetics MMA", "category": "Boxing", "location": "Neelankarai", "phone": "97911 58888", "email": "fight@combatkinetics.com", "website": "https://combatkinetics.com", "image": "https://images.unsplash.com/photo-1555597673-b21d5c935865?auto=format&fit=crop&w=800&q=80"},
        {"name": "ECR Fight Factory", "category": "Boxing", "location": "Palavakkam", "phone": "07200262666", "email": "ecrfight@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?auto=format&fit=crop&w=800&q=80"},
        {"name": "OMR Taekwondo Academy", "category": "Taekwondo Coaching Center", "location": "Kandhanchavadi", "phone": "09500020300", "email": "omrtaekwondo@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1555597673-b21d5c935865?auto=format&fit=crop&w=800&q=80"},
        {"name": "FightBack Combat Martialarts Academy", "category": "Karate", "location": "Raja Annamalaipuram", "phone": "Not available", "email": "fightback@martialarts.in", "website": "https://fightbackacademy.in", "image": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?auto=format&fit=crop&w=800&q=80"},
        {"name": "THE LEGEND MARTIAL ARTS ASSOCIATION OF INDIA", "category": "Silambam", "location": "Adambakkam", "phone": "09841101631", "email": "legend@silambam.org", "website": "https://legendsilambam.org", "image": "https://images.unsplash.com/photo-1555597673-b21d5c935865?auto=format&fit=crop&w=800&q=80"}
    ],
    "Arts & Creative Skills": [
        {"name": "Little Art Academy - Arts & Craft Class", "category": "Art School", "location": "Velachery", "phone": "9600012716", "email": "littleart@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=800&q=80"},
        {"name": "Skills Academy Of Arts & Sciences", "category": "Education Center", "location": "Madipakkam", "phone": "9751549990", "email": "skills@artsandscience.edu", "website": "https://skillsacademy.edu", "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Saraswathi Arts & Crafts Academy", "category": "Art School", "location": "Velachery", "phone": "9884135531", "email": "saraswathiarts@yahoo.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=800&q=80"},
        {"name": "Global Art Velachery", "category": "Art Center", "location": "Velachery", "phone": "7397403418", "email": "velachery@globalart.in", "website": "https://globalart.in", "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Varna Arts", "category": "Drawing Lessons", "location": "Velachery", "phone": "9499960807", "email": "varnaarts@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=800&q=80"},
        {"name": "Creative Kids Academy", "category": "Art School", "location": "Gerugambakkam", "phone": "9789070269", "email": "ckids@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Pencil Park School Of Arts", "category": "Art School", "location": "Velachery", "phone": "7845672326", "email": "info@pencilpark.in", "website": "https://pencilpark.in", "image": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=800&q=80"},
        {"name": "Shine Academy of Arts", "category": "Music School", "location": "Velachery", "phone": "7418035329", "email": "shineacademy@arts.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Online Drawing and Painting Classes (Dessin Academy)", "category": "Art School", "location": "Velachery", "phone": "7824000458", "email": "online@dessinacademy.com", "website": "https://dessinacademy.com", "image": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=800&q=80"},
        {"name": "Artistic Ruban's Center of Arts", "category": "Art School", "location": "Adyar", "phone": "08637444848", "email": "ruban@artisticcenter.com", "website": "https://artisticruban.com", "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Picasso School Of Arts", "category": "Art & Craft", "location": "Palavakkam", "phone": "09629998330", "email": "picasso@artschool.org", "website": "https://picassoarts.in", "image": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=800&q=80"},
        {"name": "Global Art Adyar", "category": "Art School", "location": "Adyar", "phone": "09952074391", "email": "adyar@globalart.in", "website": "https://globalart.in", "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Globalart Besantnagar", "category": "Art School", "location": "Besant Nagar", "phone": "09941286798", "email": "besantnagar@globalart.in", "website": "https://globalart.in", "image": "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=800&q=80"}
    ],
    "Fitness & Wellness": [
        {"name": "Sport Fit Physio Care", "category": "Healthcare", "location": "Nungambakkam", "phone": "099624 00044", "email": "physio@sportfitcare.com", "website": "https://sportfitphysio.com", "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80"},
        {"name": "Rising Fitness Health & Fitness Studio", "category": "Gym", "location": "Neelankarai", "phone": "6383177736", "email": "info@risingfitness.in", "website": "https://risingfitness.in", "image": "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Saayam Yoga Wellness", "category": "Yoga", "location": "Perungudi", "phone": "07319711261", "email": "yoga@saayamwellness.com", "website": "https://saayamwellness.com", "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80"},
        {"name": "SMART 7 Wellness", "category": "Fitness Training", "location": "Teynampet", "phone": "09940168267", "email": "smart7@wellnesshub.org", "website": "https://smart7wellness.com", "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80"},
        {"name": "Pink Fitness", "category": "Gym", "location": "Adyar", "phone": "089399 97516", "email": "care@pinkfitness.in", "website": "https://pinkfitness.in", "image": "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Harry's Fitcamp", "category": "Wellness Center", "location": "Adyar", "phone": "07200250772", "email": "fitcamp@harrys.com", "website": "https://harrysfitcamp.com", "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80"},
        {"name": "Core Bloom Wellness", "category": "Physiotherapy Center", "location": "Kilpauk", "phone": "07010302560", "email": "bloom@corewellness.org", "website": "https://corebloomwellness.com", "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80"},
        {"name": "Nine O2 Detox and Wellness Zone", "category": "Wellness Center", "location": "Thiruvanmiyur", "phone": "09940595870", "email": "detox@nineo2.com", "website": "http://nineo2wellness.com", "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=800&q=80"},
        {"name": "RS WELLNESS HUB", "category": "Wellness Center", "location": "Adyar", "phone": "Not available", "email": "rswellness@hub.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=800&q=80"}
    ],
    "Academic Coaching": [
        {"name": "Career Success Academy", "category": "NEET Coaching Centre", "location": "West Tambaram", "phone": "72006 66620", "email": "success@careersuccess.edu", "website": "https://careersuccess.edu", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"},
        {"name": "VVT Coaching Centre", "category": "NEET & JEE Coaching Centre", "location": "Adyar", "phone": "08122122333", "email": "admissions@vvtcoaching.in", "website": "https://vvtcoaching.in", "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80"},
        {"name": "Vinnmugil Academy", "category": "NEET Coaching Centre", "location": "Adyar", "phone": "09698987593", "email": "vinnmugil@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"},
        {"name": "Everwin Education", "category": "NEET And JEE Coaching Centre", "location": "Adyar", "phone": "09884964529", "email": "info@everwineducation.com", "website": "https://everwineducation.com", "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80"},
        {"name": "Appolo Academy", "category": "NEET", "location": "Velachery", "phone": "09500704040", "email": "appolo@neetcoaching.org", "website": "https://appoloacademy.com", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"},
        {"name": "SRI ABIRAMI TUITION CENTRE", "category": "Education Center", "location": "Thiruvanmiyur", "phone": "09500038291", "email": "abirami@tuition.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80"},
        {"name": "LORD'S ACADEMY TUITION CENTER", "category": "Tuition Center", "location": "Thiruvanmiyur", "phone": "09677150405", "email": "lords@tuitioncenter.org", "website": "Not available", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"},
        {"name": "Sri Abirami Tuition", "category": "Education Center", "location": "Thiruvanmiyur", "phone": "09500038291", "email": "abirami2@tuition.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80"},
        {"name": "MathTonics Academy", "category": "Education Center", "location": "Adyar", "phone": "09080575330", "email": "mathtonics@maths.edu", "website": "https://mathtonics.com", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"},
        {"name": "Lords Tuition Centre", "category": "Private Tutor", "location": "Thiruvanmiyur", "phone": "Not available", "email": "lordstutor@gmail.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80"},
        {"name": "Veranda IAS", "category": "UPSC Coaching", "location": "Nandanam", "phone": "8925521735", "email": "support@verandalearning.com", "website": "https://verandalearning.com", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"},
        {"name": "RADIAN IAS ACADEMY", "category": "UPSC Coaching", "location": "West Tambaram", "phone": "8608099530", "email": "radian@iasacademy.com", "website": "https://radianiasacademy.com", "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80"},
        {"name": "All India Civil Services Coaching Centre", "category": "Coaching Centre", "location": "Raja Annamalaipuram", "phone": "04424621909", "email": "aicscc@tn.gov.in", "website": "https://civilservicecoaching.tn.gov.in", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"},
        {"name": "Shankar IAS Academy Adyar", "category": "Coaching Centre", "location": "Adyar", "phone": "9025278278", "email": "info@shankariasacademy.com", "website": "https://shankariasacademy.com", "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80"},
        {"name": "Raja Sir's Cracking IAS Academy", "category": "Coaching Centre", "location": "Anna Nagar", "phone": "9962527528", "email": "rajasir@crackingias.org", "website": "https://crackingias.org", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"},
        {"name": "Kamaraj IAS Academy", "category": "Coaching Centre", "location": "Anna Nagar", "phone": "04443539988", "email": "kamaraj@iasacademy.in", "website": "https://kamarajias.com", "image": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80"},
        {"name": "KINGMAKERS IAS ACADEMY", "category": "Coaching Centre", "location": "Anna Nagar", "phone": "9444227273", "email": "info@kingmakersias.com", "website": "https://kingmakersias.com", "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=800&q=80"}
    ],
    "Other Skill Development": [
        {"name": "Action DnA", "category": "Acting", "location": "Mylapore", "phone": "089258 39828", "email": "info@actiondna.in", "website": "https://actiondna.in", "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Public Speaking Skills Chennai", "category": "Training Center", "location": "T. Nagar", "phone": "09282239388", "email": "speaking@skills.org", "website": "Not available", "image": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=800&q=80"},
        {"name": "Success Next", "category": "Personality Development", "location": "Nungambakkam", "phone": "Not available", "email": "next@success.com", "website": "Not available", "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Personality Development Training Classes Center", "category": "Training Center", "location": "Little Mount", "phone": "Not available", "email": "pd@classes.in", "website": "Not available", "image": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=800&q=80"},
        {"name": "Ramanathans", "category": "Group Discussions", "location": "Adyar", "phone": "09840786269", "email": "contact@ramanathans.com", "website": "https://ramanathans.com", "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&q=80"},
        {"name": "SUPERBHUMANS (Purasawalkam)", "category": "Personality Development", "location": "Purasaiwakkam", "phone": "09840130430", "email": "purasa@superbhumans.org", "website": "https://superbhumans.org", "image": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=800&q=80"},
        {"name": "SUPERBHUMANS (Anna Nagar)", "category": "Personality Development", "location": "Anna Nagar West Extension", "phone": "09840130430", "email": "annanagar@superbhumans.org", "website": "https://superbhumans.org", "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Core Growth Pivot", "category": "Soft Skills", "location": "Aminjikarai", "phone": "09841308888", "email": "growth@corepivot.com", "website": "https://coregrowthpivot.com", "image": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=800&q=80"},
        {"name": "Master Yourself Academy", "category": "NLP Training", "location": "Nandanam", "phone": "09566942555", "email": "nlp@masteryourself.in", "website": "https://masteryourself.in", "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=800&q=80"},
        {"name": "Speaking Ninjas", "category": "Learning Center", "location": "Akshaya 36 Carat", "phone": "09884064668", "email": "ninja@speaking.com", "website": "https://speakingninjas.com", "image": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=800&q=80"}
    ]
}
AUTH_STYLE = """
    <style>
        :root {
            --primary: #1e3a8a;
            --accent: #d97706;
            --bg-soft: #f8fafc;
            --card-border: #e2e8f0;
        }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #9a3412 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            margin: 0;
        }
        .auth-card {
            background: #ffffff;
            border-radius: 20px;
            padding: 32px;
            width: 100%;
            max-width: 420px;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.28);
            border: 1px solid var(--card-border);
        }
        .auth-title {
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 6px;
        }
        .auth-sub {
            color: #64748b;
            font-size: 0.92rem;
            margin-bottom: 22px;
        }
        .form-control {
            border-radius: 12px;
            padding: 11px 14px;
            border: 1px solid #cbd5e1;
        }
        .btn-auth {
            background: linear-gradient(135deg, #1e3a8a, #d97706);
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 11px 18px;
            font-weight: 600;
            width: 100%;
        }
        .btn-auth:hover {
            color: #fff;
            opacity: 0.95;
        }
    </style>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login — Chennai Academy Directory</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
""" + AUTH_STYLE + """
</head>
<body>
    <div class="auth-card">
        <h2 class="auth-title">Welcome Back</h2>
        <p class="auth-sub">Login to access Chennai Academy Directory</p>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} py-2 small">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST">
            <div class="mb-3">
                <label class="form-label small fw-semibold">Email</label>
                <input type="email" name="email" class="form-control" required placeholder="you@example.com">
            </div>
            <div class="mb-3">
                <label class="form-label small fw-semibold">Password</label>
                <input type="password" name="password" class="form-control" required placeholder="••••••••">
            </div>
            <button type="submit" class="btn btn-auth mt-1">Login</button>
        </form>

        <p class="text-center small text-muted mt-4 mb-0">
            New here? <a href="{{ url_for('register') }}" class="fw-semibold text-decoration-none">Create an account</a>
        </p>
    </div>
</body>
</html>
"""

REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register — Chennai Academy Directory</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
""" + AUTH_STYLE + """
</head>
<body>
    <div class="auth-card">
        <h2 class="auth-title">Create Account</h2>
        <p class="auth-sub">Register to explore academies across Chennai</p>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} py-2 small">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST">
            <div class="mb-3">
                <label class="form-label small fw-semibold">Full Name</label>
                <input type="text" name="name" class="form-control" required placeholder="Your name">
            </div>
            <div class="mb-3">
                <label class="form-label small fw-semibold">Email</label>
                <input type="email" name="email" class="form-control" required placeholder="you@example.com">
            </div>
            <div class="mb-3">
                <label class="form-label small fw-semibold">Password</label>
                <input type="password" name="password" class="form-control" required minlength="6" placeholder="At least 6 characters">
            </div>
            <button type="submit" class="btn btn-auth mt-1">Register</button>
        </form>

        <p class="text-center small text-muted mt-4 mb-0">
            Already have an account? <a href="{{ url_for('login') }}" class="fw-semibold text-decoration-none">Login</a>
        </p>
    </div>
</body>
</html>
"""

HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academy Directory — Chennai</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #1e3a8a;
            --accent: #d97706;
            --bg-soft: #f8fafc;
            --card-border: #e2e8f0;
        }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-soft);
            color: #1e293b;
            margin: 0;
            padding-bottom: 50px;
        }
        .hero-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #9a3412 100%);
            color: #ffffff;
            padding: 36px 20px 46px;
            margin-bottom: 32px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.18);
        }
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
            font-size: 0.92rem;
        }
        .hero-header h1 {
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }
        .hero-header p {
            color: #e2e8f0;
            margin-bottom: 0;
            font-size: 1.05rem;
        }
        .search-box {
            background: #ffffff;
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
            border: 1px solid var(--card-border);
            margin-bottom: 40px;
        }
        .form-control, .form-select {
            border-radius: 12px;
            padding: 12px 16px;
            border: 1px solid #cbd5e1;
        }
        .btn-search {
            background: linear-gradient(135deg, #1e3a8a, #d97706);
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
        }
        .btn-search:hover {
            color: #fff;
            opacity: 0.94;
        }
        .section-title {
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 22px;
            padding-left: 12px;
            border-left: 5px solid var(--accent);
        }
        .dir-card {
            background: #ffffff;
            border: 1px solid var(--card-border);
            border-radius: 16px;
            overflow: hidden;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
            transition: transform 0.22s ease, box-shadow 0.22s ease;
        }
        .dir-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 14px 28px rgba(15, 23, 42, 0.12);
        }
        .card-img-wrap {
            position: relative;
            height: 185px;
            overflow: hidden;
            background: #e2e8f0;
        }
        .card-img-wrap img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .badge-count {
            position: absolute;
            top: 12px;
            right: 12px;
            background: rgba(15, 23, 42, 0.82);
            color: #fff;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .badge-loc {
            background: #fef3c7;
            color: #92400e;
            font-weight: 600;
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.78rem;
            display: inline-block;
            margin-bottom: 8px;
        }
        .card-body-custom {
            padding: 18px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .card-title-custom {
            font-size: 1.12rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
        }
        .meta-line {
            font-size: 0.9rem;
            color: #475569;
            margin-bottom: 6px;
        }
        .card-link-stretched {
            text-decoration: none;
            color: inherit;
        }
        .website-btn {
            margin-top: auto;
            padding-top: 10px;
        }
    </style>
    <link rel="manifest" href="/static/manifest.json">
    <script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/static/sw.js');
    });
  }
</script>
</head>
<body>
    <div class="hero-header">
        <div class="container">
            <div class="top-bar">
                <span>Welcome, <strong>{{ user_name }}</strong></span>
                <a href="{{ url_for('logout') }}" class="btn btn-sm btn-outline-light rounded-pill px-3">Logout</a>
            </div>
            <div class="text-center">
                <h1>Chennai Academy Directory</h1>
                <p>Sports, Dance, Music, Coding, Martial Arts, Arts, Fitness & Coaching in one clean place</p>
            </div>
        </div>
    </div>

    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="search-box">
            <form method="GET" action="/" class="row g-3 align-items-center">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Search by academy name, skill, or category..." value="{{ query }}">
                </div>
                <div class="col-md-4">
                    <select name="location" class="form-select">
                        <option value="">All Locations</option>
                        {% for loc in all_locations %}
                        <option value="{{ loc }}" {% if loc == selected_location %}selected{% endif %}>{{ loc }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2 d-grid">
                    <button type="submit" class="btn btn-search">Search</button>
                </div>
            </form>
        </div>

        {% if query or selected_location %}
            <h2 class="section-title">Search Results</h2>

            {% if matching_categories %}
            <h4 class="mb-3 fw-semibold text-secondary">Matching Categories</h4>
            <div class="row g-4 mb-5">
            {% for cat_name in matching_categories %}
                <div class="col-sm-6 col-lg-4">
                    <a href="/category/{{ cat_name }}" class="card-link-stretched">
                        <div class="dir-card">
                            <div class="card-img-wrap">
                                <img src="{{ category_images[cat_name] }}" alt="{{ cat_name }}">
                                <span class="badge-count">{{ academies_data[cat_name]|length }} Academies</span>
                            </div>
                            <div class="card-body-custom">
                                <h3 class="card-title-custom">{{ cat_name }}</h3>
                                <p class="meta-line mb-0">Explore academies →</p>
                            </div>
                        </div>
                    </a>
                </div>
            {% endfor %}
            </div>
            {% endif %}

            <h4 class="mb-3 fw-semibold text-secondary">Matching Academies</h4>
            <div class="row g-4">
            {% for acc in matching_academies %}
                <div class="col-sm-6 col-lg-4">
                    <div class="dir-card">
                        <div class="card-img-wrap">
                            <img src="{{ acc.image }}" alt="{{ acc.name }}">
                        </div>
                        <div class="card-body-custom">
                            <span class="badge-loc">{{ acc.location }}</span>
                            <h3 class="card-title-custom">{{ acc.name }}</h3>
                            <p class="meta-line"><strong>Category:</strong> {{ acc.category }}</p>
                            <p class="meta-line"><strong>Phone:</strong> {{ acc.phone }}</p>
                            <p class="meta-line"><strong>Email:</strong> {{ acc.email }}</p>
                            <div class="website-btn">
                                {% if acc.website != 'Not available' %}
                                    <a href="{{ acc.website }}" target="_blank" class="btn btn-sm btn-outline-primary rounded-pill px-3">Visit Website</a>
                                {% else %}
                                    <span class="text-muted small">Website not available</span>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>
            {% else %}
                <div class="col-12">
                    <div class="alert alert-light border text-center py-4">No matching academies found.</div>
                </div>
            {% endfor %}
            </div>

        {% else %}
            <h2 class="section-title">All Categories</h2>
            <div class="row g-4">
            {% for category, items in academies_data.items() %}
                <div class="col-sm-6 col-lg-4">
                    <a href="/category/{{ category }}" class="card-link-stretched">
                        <div class="dir-card">
                            <div class="card-img-wrap">
                                <img src="{{ category_images[category] }}" alt="{{ category }}">
                                <span class="badge-count">{{ items|length }} Academies</span>
                            </div>
                            <div class="card-body-custom">
                                <h3 class="card-title-custom">{{ category }}</h3>
                                <p class="meta-line mb-0">View all listings →</p>
                            </div>
                        </div>
                    </a>
                </div>
            {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
'''
DETAIL_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ category }} — Chennai Academy Directory</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #1e3a8a;
            --accent: #d97706;
            --bg-soft: #f8fafc;
            --card-border: #e2e8f0;
        }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-soft);
            color: #1e293b;
            margin: 0;
            padding-bottom: 50px;
        }
        .page-banner {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #9a3412 100%);
            color: #ffffff;
            padding: 28px 20px 36px;
            margin-bottom: 32px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.16);
        }
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 16px;
            font-size: 0.92rem;
        }
        .page-banner h1 {
            font-weight: 800;
            margin-bottom: 6px;
        }
        .back-btn {
            color: #fde68a;
            text-decoration: none;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
        }
        .back-btn:hover {
            color: #ffffff;
            text-decoration: underline;
        }
        .search-box {
            background: #ffffff;
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
            border: 1px solid var(--card-border);
            margin-bottom: 36px;
        }
        .form-control, .form-select {
            border-radius: 12px;
            padding: 12px 16px;
            border: 1px solid #cbd5e1;
        }
        .btn-search {
            background: linear-gradient(135deg, #1e3a8a, #d97706);
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
        }
        .btn-search:hover {
            color: #fff;
            opacity: 0.94;
        }
        .dir-card {
            background: #ffffff;
            border: 1px solid var(--card-border);
            border-radius: 16px;
            overflow: hidden;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
            transition: transform 0.22s ease, box-shadow 0.22s ease;
        }
        .dir-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 14px 28px rgba(15, 23, 42, 0.12);
        }
        .card-img-wrap {
            height: 185px;
            overflow: hidden;
            background: #e2e8f0;
        }
        .card-img-wrap img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .badge-loc {
            background: #fef3c7;
            color: #92400e;
            font-weight: 600;
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.78rem;
            display: inline-block;
            margin-bottom: 8px;
        }
        .card-body-custom {
            padding: 18px;
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .card-title-custom {
            font-size: 1.12rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 8px;
        }
        .meta-line {
            font-size: 0.9rem;
            color: #475569;
            margin-bottom: 6px;
        }
        .website-btn {
            margin-top: auto;
            padding-top: 10px;
        }
    </style>
    <link rel="manifest" href="/static/manifest.json">
    <script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/static/sw.js');
    });
  }
</script>
</head>
<body>
    <div class="page-banner">
        <div class="container">
            <div class="top-bar">
                <span>Welcome, <strong>{{ user_name }}</strong></span>
                <a href="{{ url_for('logout') }}" class="btn btn-sm btn-outline-light rounded-pill px-3">Logout</a>
            </div>
            <a href="/" class="back-btn">← Back to All Categories</a>
            <h1>{{ category }}</h1>
            <p class="mb-0 text-light">{{ academies|length }} academies listed</p>
        </div>
    </div>

    <div class="container">
        <div class="search-box">
            <form method="GET" action="/category/{{ category }}" class="row g-3 align-items-center">
                <div class="col-md-6">
                    <input type="text" name="q" class="form-control" placeholder="Search academies in this category..." value="{{ query }}">
                </div>
                <div class="col-md-4">
                    <select name="location" class="form-select">
                        <option value="">All Locations</option>
                        {% for loc in all_locations %}
                        <option value="{{ loc }}" {% if loc == selected_location %}selected{% endif %}>{{ loc }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2 d-grid">
                    <button type="submit" class="btn btn-search">Search</button>
                </div>
            </form>
        </div>

        <div class="row g-4">
            {% for acc in academies %}
            <div class="col-sm-6 col-lg-4">
                <div class="dir-card">
                    <div class="card-img-wrap">
                        <img src="{{ acc.image }}" alt="{{ acc.name }}">
                    </div>
                    <div class="card-body-custom">
                        <span class="badge-loc">{{ acc.location }}</span>
                        <h3 class="card-title-custom">{{ acc.name }}</h3>
                        <p class="meta-line"><strong>Category:</strong> {{ acc.category }}</p>
                        <p class="meta-line"><strong>Phone:</strong> {{ acc.phone }}</p>
                        <p class="meta-line"><strong>Email:</strong> {{ acc.email }}</p>
                        <div class="website-btn">
                            {% if acc.website != 'Not available' %}
                                <a href="{{ acc.website }}" target="_blank" class="btn btn-sm btn-outline-primary rounded-pill px-3">Visit Website</a>
                            {% else %}
                                <span class="text-muted small">Website not available</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
            {% else %}
                <div class="col-12">
                    <div class="alert alert-light border text-center py-4">No matching academies found in this category.</div>
                </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

def get_all_locations():
    locs = set()
    for items in academies_data.values():
        for item in items:
            locs.add(item['location'])
    return sorted(list(locs))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not name or not email or len(password) < 6:
            flash("Please fill in all fields properly (password must be at least 6 characters).", "danger")
            return render_template_string(REGISTER_TEMPLATE)

        conn = get_db_connection()
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            conn.close()
            flash("This email is already registered. Please log in.", "warning")
            return redirect(url_for("login"))

        password_hash = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        conn.close()

        flash("Registration successful! Please log in now.", "success")
        return redirect(url_for("login"))

    return render_template_string(REGISTER_TEMPLATE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            flash("Logged in successfully!", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("home"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route('/')
@login_required
def home():
    query = request.args.get('q', '').strip().lower()
    selected_location = request.args.get('location', '').strip()
    all_locations = get_all_locations()

    matching_categories = []
    matching_academies = []

    if query or selected_location:
        for category, items in academies_data.items():
            if query and query in category.lower():
                matching_categories.append(category)

            for acc in items:
                matches_query = not query or (
                    query in acc['name'].lower()
                    or query in acc['category'].lower()
                    or query in acc['location'].lower()
                )
                matches_loc = not selected_location or acc['location'] == selected_location

                if matches_query and matches_loc and acc not in matching_academies:
                    matching_academies.append(acc)

    return render_template_string(
        HOME_TEMPLATE,
        user_name=session.get("user_name", "User"),
        academies_data=academies_data,
        category_images=CATEGORY_IMAGES,
        query=query,
        selected_location=selected_location,
        all_locations=all_locations,
        matching_categories=matching_categories,
        matching_academies=matching_academies,
    )

@app.route('/category/<category_name>')
@login_required
def category_detail(category_name):
    query = request.args.get('q', '').strip().lower()
    selected_location = request.args.get('location', '').strip()
    all_locations = get_all_locations()
    all_academies = academies_data.get(category_name, [])

    academies = []
    for acc in all_academies:
        matches_query = not query or (
            query in acc['name'].lower()
            or query in acc['category'].lower()
            or query in acc['location'].lower()
        )
        matches_loc = not selected_location or acc['location'] == selected_location
        if matches_query and matches_loc:
            academies.append(acc)

    return render_template_string(
        DETAIL_TEMPLATE,
        user_name=session.get("user_name", "User"),
        category=category_name,
        academies=academies,
        query=query,
        selected_location=selected_location,
        all_locations=all_locations,
    )

if __name__ == '__main__':
    app.run(debug=True)
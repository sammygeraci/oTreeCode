from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label="Age: ")
    gender = models.StringField(label="Gender: ", choices=["MALE", "FEMALE", "OTHER"])
    race = models.StringField(label="Race/Ethnicity: ",
                              choices=["Hispanic or Latino", "American Indian or Alaska Native", "Asian",
                                       "Black or African American", "Native Hawaiian or other Pacific Islander",
                                       "White", "Prefer not to say"])
    grade = models.IntegerField(label="Year in college including undergraduate and graduate studies:", choices=[
        [1, "First Year Student"],
        [2, "Second Year Student"],
        [3, "Third Year Student"],
        [4, "Fourth Year Student"],
        [5, "Fifth Year Student"],
        [6, "Sixth Year Student"],
        [7, "Seventh Year Student or Higher"],
        [8, "Not attending college currently"]
    ])
    major = models.StringField(label="Primary Undergraduate Degree: ", choices=[
        "Accounting, BS",
        "Addiction and Recovery, BS",
        "Advertising, BA",
        "Aerospace Engineering, BS",
        "African American Studies, BA",
        "American Studies, BA",
        "Anthropology, BA",
        "Apparel and Textiles, BS",
        "Applied Liberal Arts and Sciences, BA",
        "Architectural Engineering, BS",
        "Art History, BA",
        "Biology, BS",
        "Business Cyber Security, BS",
        "Chemical Engineering, BSChE",
        "Chemistry, BCH",
        "Chemistry, BS",
        "Civil Engineering, BS",
        "Collaborative Education Program, BSE",
        "Communication Studies, BAC",
        "Communicative Disorders, BA",
        "Computer Engineering, BS",
        "Computer Science, BS",
        "Construction Engineering, BS",
        "Consumer Sciences, BS",
        "Creative Media, BA",
        "Criminology & Criminal Justice, BA",
        "Cyber Security, BS",
        "Dance, BA",
        "Early Childhood Education, BS",
        "Early Childhood Special Education",
        "Economics, BA",
        "Economics, BS",
        "Educational Neuroscience, BS",
        "Electrical Engineering, BS",
        "Elementary Education, BSE",
        "English, BA",
        "Environmental Engineering, BS",
        "Environmental Science, BS",
        "Finance, BS",
        "Food and Nutrition, BS",
        "Foreign Languages and Literature, BA",
        "General Business, BS",
        "Geography, BA",
        "Geography, BS",
        "Geology, BA",
        "Geology, BS",
        "Geology, BSG",
        "Graphic Design, BFA",
        "History, BA",
        "Hospitality Management, BS",
        "Human Development and Family Studies, BS",
        "Human Environmental Sciences, BS",
        "Interdisciplinary Studies, BA",
        "Interdisciplinary Studies, BS",
        "Interior Design, BS",
        "International Studies, BA",
        "Kinesiology, BS",
        "Management Information Systems, BS",
        "Management, BS",
        "Manufacturing Systems Engineering, BS",
        "Marine Science, BS",
        "Marketing, BS",
        "Mathematics, BS",
        "Mechanical Engineering, BS",
        "Metallurgical Engineering, BS",
        "Microbiology, BS",
        "Multiple Abilities Program, BSE",
        "Music Composition, BM",
        "Music Education, BSE (Certification in Instrumental Music)",
        "Music Education, BSE (Certification in Vocal/Choral Music)",
        "Music Performance, BM",
        "Music Theory, BM",
        "Music Therapy, BM",
        "Music with a concentration in Arts Administration, BA",
        "Music, BA",
        "Musical Audio Engineering, BS",
        "Neuroscience, BS",
        "News Media, BA",
        "Nursing (RN to BSN)",
        "Nursing, BSN",
        "Operations Management, BS",
        "Philosophy, BA",
        "Physics, BS",
        "Political Science, BA",
        "Psychology, BA",
        "Psychology, BS",
        "Public Health, BS",
        "Public Relations, BA",
        "Religious Studies, BA",
        "Secondary Education, BSE",
        "Social Work, BSW",
        "Spanish, BA",
        "Sport Management, BS",
        "Studio Art, BA",
        "Studio Art, BFA",
        "Theatre with a Musical Theatre Concentration, BA",
        "Theatre, BA",
        "Theatre, BFA",
        "Undecided",
        "Other"
    ])
    other_major = models.StringField(label="If other, enter degree program: ", blank=True)
    state = models.StringField(label="State of origin (state where you graduated high school): ", choices=[
        "I did not graduate high school in the United States.",
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
        "Washington District of Colombia",
        "American Samoa",
        "Guam",
        "Northern Mariana Islands",
        "Puerto Rico",
        "U.S. Virgin Islands"
    ])
    CRTQ1 = models.CurrencyField(label="Q1. A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the "
                                       "ball. How much does the ball cost? (in dollars) ")
    CRTQ2 = models.IntegerField(label="If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 "
                                      "machines to make 100 widgets? (in minutes)")
    CRTQ3 = models.IntegerField(label="In a lake, there is a patch of lily pads. Every day, the patch doubles in "
                                      "size. If it takes 48 days for the patch to cover the entire lake, "
                                      "how long would it take for the patch to cover half of the lake? (in days)")
    CRT_Score = models.IntegerField(initial=0)


# PAGES
class Stop(Page):
    pass


class MyPage(Page):
    form_model = "player"
    form_fields = ['age', 'gender', 'race', 'grade', 'major', 'other_major', 'state']


class CRTSurvey(Page):
    form_model = "player"
    form_fields = ['CRTQ1', 'CRTQ2', 'CRTQ3']

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.CRTQ1 == cu(0.05):
            player.CRT_Score += 1
        if player.CRTQ2 == 5:
            player.CRT_Score += 1
        if player.CRTQ3 == 47:
            player.CRT_Score += 1


page_sequence = [Stop, MyPage, CRTSurvey]

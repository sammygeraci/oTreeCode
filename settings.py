from os import environ

SESSION_CONFIGS = [
    dict(
        name='LuckEgalitariansVsRelationalEgalitariansInTheLotteryGame',
        app_sequence=['DictatorGame', 'IndividualContest', 'RiskTolerance', 'survey', 'ExplainPayoff'],
        num_demo_participants=2,
    ),
]

ROOMS = [
    dict(
        name='Tide_Lab',
        display_name='Behavioral Economics Lab'
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['persistent_id', 'risk_x', 'risk_pi', 'risk_flip', 'final_round_num', 'round_pi', 'round_a', 'round_r', 'round_x', 'round_opponent_x',
                      'round_win', 'round_color']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4467741448104'

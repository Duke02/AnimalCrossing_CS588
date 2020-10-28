from os.path import join

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the community data spreadsheet.
SPREADSHEET_ID = '1hMmewPJvXw-tmabvccC0nWJdN7zw3aQIQzN3EQ9is6g'
CELL_RANGE = 'Archive!C:S'

# The minimum number of prices required to have been gathered to make a decision.
MIN_NUM_PRICES: int = 4

# The random state to use across all models.
# 13 is my favorite number, thus its selection.
RANDOM_STATE: int = 13

SVM_ITERATIONS: int = int(1000 ** 1.5)

CV: int = 3

MODEL_FILEPATH: str = join('.', 'models')

N_JOBS: int = -1

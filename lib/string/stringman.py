import re

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def SearchReplace(text, replacement):
    for key, val in replacement.items():
        text = text.replace(key, val)
    return text

# The name has to be an alpha or number
def checkName(name):
    return name.isalnum()

def checkVersion(version):
    pattern = re.compile("v[0-9]+\.[0-9]+\.[0-9]+\-(alpha|beta)(\.[0-9]+)?")
    return pattern.match(version) is not None

def checkStage(currentState, maxStage):
    return (currentState <= maxStage) and (currentState >= 0)
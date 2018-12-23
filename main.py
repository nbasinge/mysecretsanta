from functions import *

users = scanTable('secretsanta')
year = '2018'
# print(users)
secretSantas = secretSanta(users['Items'])
if secretSantas == 'bad_combination':
    print('exiting, bad combination. Try again')
else:
    # print(secretSantas)
    validated = testValidSecretSanta(secretSantas)
    if validated:
        for santa in secretSantas:
            name = santa['name']['S']
            phonenumber = santa['number']['S']
            secretSanta = santa['secretsanta']
            # print('{} picked {}'.format(name,secretSanta))
            subject = 'Secret Santa'
            message = "Hi {}, you have {} for Secret Santa {}. Good Luck! We're all counting on you.".format(name, secretSanta, year)
            addSecretSanta(name,secretSanta,'secretsanta')
            sendtext(name, phonenumber, subject, message)
        print('no error occurred validating')
    else:
        print('error occurred validating')

print('application complete')

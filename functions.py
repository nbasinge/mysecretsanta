import random, boto3, time
sns = boto3.client('sns')
dynamodb = boto3.client('dynamodb')

def sendtext(name, phonenumber, subject, message):
    # print name
    # print phonenumber
    # print subject
    # print message
    response = sns.publish(PhoneNumber='+1' + phonenumber, Message=message)
    # print response

def addSecretSanta(name, secretSanta, tableName):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)

    response = table.update_item(
    Key={
        'name': name,
    },
    UpdateExpression="set currentSecretSanta = :c",
    ExpressionAttributeValues={
        ':c': secretSanta,
    },
    ReturnValues="UPDATED_NEW"
    )

def getSecretSanta(tableName, name):
    users = scanTable(tableName)['Items']
    secretSanta = [x['currentSecretSanta'] for x in users if x['name']['S']==name]
    print('Your secret santa is {}'.format(secretSanta))

def secretSanta(users):
    for user in users:
        if 'secretsanta' in user:
            del user['secretsanta']

    secretsantasleft = []
    for santa in users:
        # print santa
        secretsantasleft.append(santa['name']['S'])

    santastokill = []
    for user in users:
        if 'norm' in user:
            secretsanta = str(user['norm']['S'])
            user['secretsanta'] = secretsanta
            # print 'picked'
            # print secretsanta
            santastokill.append(secretsanta)

    for user in users:
        if santastokill:
            for kill in santastokill:
                secretsantasleft.remove(kill)

            santastokill = []
        # print user
        name = str(user['name']['S'])
        if 'mate' in user:
            hasmate = True
            mate = str(user['mate']['S'])
            # print 'has mate'
        else:
            hasmate = False
        # print 'picker'
        # print name
        picknotself = False
        picknotmate = False
        if 'secretsanta' not in user:
            while picknotself == False or picknotmate == False:
                picknotself = False
                picknotmate = False
                secretsanta = random.choice(secretsantasleft)
                # # print 'picked'
                # # print secretsanta
                if secretsanta != name:
                    picknotself = True
                    # # print 'didnt pick self'
                else:
                    if secretsanta == name and len(secretsantasleft) > 1:
                        # print secretsantasleft
                        print 'picked self, try again...'
                    else:
                        print name + ' cant pick ' + secretsanta + ' but they are only name left'
                        time.sleep(3)
                        return 'bad_combination'
                if hasmate == True:
                    if secretsanta != mate:
                        picknotmate = True
                        # print 'didnt pick mate'
                    elif secretsanta == mate and len(secretsantasleft) > 1 or len(secretsantasleft) == 2 and name not in secretsantasleft:
                        # print secretsantasleft
                        print 'picked mate, try again...'
                    else:
                        if secretsanta == mate and len(secretsantasleft) == 2 and name in secretsantasleft:
                            print name + ' cant pick ' + secretsanta + ' but they are my mate and we are the only people left to pick!'
                            time.sleep(3)
                            return 'bad_combination'
                        print name + ' cant pick ' + secretsanta + ' but they are only name left'
                        time.sleep(3)
                        return 'bad_combination'
                else:
                    picknotmate = True
                    # print 'has no mate'
                if picknotmate == True and picknotself == True:
                    user['secretsanta'] = secretsanta
                    santastokill.append(secretsanta)

    return users


def testValidSecretSanta(users):
    santaspicked = []
    print 'checking if bad picks occurred (self or mate)'
    for user in users:
        nothaveself = False
        nothavemate = False
        # print 'validating users...'
        santaspicked.append(user['secretsanta'])
        if user['name']['S'] != user['secretsanta']:
            # print user['name']['S'] + ' passed the doesnt have yourself check'
            nothaveself = True
        if 'mate' in user:
            if user['mate']['S'] != user['secretsanta']:
                # print user['name']['S'] + ' passed the doesnt have own mate check'
                nothavemate = True
        else:
            nothavemate = True
        if nothaveself == False or nothavemate == False:
            print 'PICKED BAD PERSON ERROR OCCURED' + str(user)
            return False

    # print 'checking if everyone was picked'
    for user in users:
        if user['name']['S'] not in santaspicked:
            print 'NOBODY PICKED ME ERROR OCCURED' + str(user)
            return False

    # add another validate for not picking last years person (using persistent store aka database)

    print 'everyone was picked!'
    print 'checking that no one was picked more than once'
    if len(santaspicked) == len(set(santaspicked)):
        print 'nobody was picked more than once'
    else:
        print 'SOMEONE PICKED MORE THAN ONCE ERROR OCCURED' + str(user)
        return False
    return True


def scanTable(table):
    initialtableresponse = dynamodb.scan(TableName=table)
    return initialtableresponse

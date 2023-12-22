import json 

ROOT_PROJECT = "/home/ghost/PycharmProjects/project_Imc"

def load_data(name):
    with open(f'{ROOT_PROJECT}/{name}', 'r') as f:
        return json.load(f)


def save_data(name, object):
    with open(f'{ROOT_PROJECT}/{name}', 'w') as f:
        json.dump(object, f)


def get_users_data(id_, users, datas):
    user = [user1 for user1 in users if id_ == user1['id']][0]
    data = [data_ for data_ in datas if id_ == data_['user_id']][0]
    
    users_index = users.index(user)
    user_data_index = datas.index(data)
    
    return user, data, users_index ,user_data_index


def imc_calculator(taille, poids):
    return round(poids/taille**2, 2)


def default_input(name, default):
    val =  input(name)
    return val if val else default


def get_sante_class(imc):
    class_sante = None
    if 18.5 <= imc <= 24.9:
        class_sante = 0
    elif imc < 18.5:
        class_sante = 1
    elif 25 <= imc <= 30:
        class_sante = 2
    elif 30 <= imc <= 35:
        class_sante = 3
    elif 35 <= imc <= 40:
        class_sante = 4
    else:
        class_sante = 5
        
    return class_sante

def main():
    print("Bonjour Mr/Mme comment allez-vous\n")
    print("Veuillez vous conneté\n")
    print("1- connexion")
    print("2- creer un compte\n")
    
    option = int(input(''))
    if option == 1:
        users = load_data('users.json')
        datas = load_data('datas.json')
        
        for user in users:
            print(f"{user['id']} - {user['nom']} {user['prenom']}")
        user_id = int(input(''))
        print("Que souhaitez vous ?: ")
        print("1- Modification de données")
        print("2- verification IMC")
        print("3- Etat de santé ")
        
        action = int(input(''))
        
        if action == 1:
            user, data, user_index, user_data_index = get_users_data(user_id, users, datas)
            
            user['nom'] = default_input('Nom ', user['nom'])
            user['prenom'] = default_input('Prenom ', user['prenom'])
            user['age'] = default_input('Age ', user['age'])
            user['sexe'] = default_input('Sexe ', user['sexe'])
            user['travail'] = default_input('Travail ', user['travail'])
            
            data['data']['taille'] = int(default_input('Taille (Cm) ', data['data']['taille']*100))/100
            data['data']['poids'] = int(default_input('Poids (Kg) ', data['data']['poids']))
            
            imc = imc_calculator(data['data']['taille'], data['data']['poids'])
            
            data['data']['imc'] = imc
            
            datas[user_data_index] = data
            users[user_index] = user 
            
            data['data']['class_sante'] = get_sante_class(imc)
            
            save_data('datas.json', datas)
            save_data('users.json', users)
            
            pass
        elif action == 2:
            user, data, user_index, user_data_index = get_users_data(user_id, users, datas)
            print(data['data']['imc'])
            pass
        elif action == 3:
            santes = load_data('sante.json')
            user, data, user_index, user_data_index = get_users_data(user_id, users, datas)
            user_sante = [sante for sante in santes if sante['id'] == data['data']['class_sante']][0]
            print(f"Etat : {user_sante['maladie']}\n")
            print(f"Analyse : {user_sante['reason']}\n")
            print(f"Conseil : {user_sante['conseil']}\n")
            
            pass
        else:
            print("Valeur non reconnue")
    if option == 2:
        users = load_data('users.json')
        datas = load_data('datas.json')
        
        user = {}
        data = {'data' : {}}
        user_id = None
        
        try:
            user_id = users[-1]['id'] + 1
            pass
        except IndexError:
            user_id = 1
            pass
        
        user['id'] = user_id
        user['nom'] = default_input('Nom ', f"Utilisateur {user_id}")
        user['prenom'] = input('Prenom ')
        user['age'] = input('Age ')
        user['sexe'] = input('Sexe ')
        user['travail'] = input('Travail ')
            
        data['data']['taille'] = float(input('Taille (Cm) '))/100
        data['data']['poids'] = float(input('Poids (Kg) '))
        
        imc = imc_calculator(data['data']['taille'], data['data']['poids'])
        
        data['user_id'] = user['id']   
        data['data']['imc'] = imc 
            
        data['data']['class_sante'] = get_sante_class(imc)
        
        users.append(user)
        datas.append(data)
        
        save_data('users.json', users)
        save_data('datas.json', datas)
        
        pass
    
main()
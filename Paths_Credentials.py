import pickle
import os

def Path(Credentials_file = 'Credentials/Credentials.pkl'):
    try:
        f = open(Credentials_file, 'rb')
        Credentials = pickle.load(f)
        f.close()
    except:
        Credentials = {}
        # Get save path
        Credentials['csv_save_path'] = input(
            'Please copy and paste the path to the folder to save the DD_update files.\nPath:').replace('\\', '/') + '/'
        Credentials['main_path'] = input(
            'Please copy and paste the path to the folder of the Main.py file.\nPath:').replace('\\', '/') + '/'
        # Save API Key and BNED OneDrive path in credentials file
        os.makedirs('Credentials', exist_ok=True)
        f = open(Credentials_file, 'wb')
        pickle.dump(Credentials, f)
        f.close()

    return Credentials


def Verba_Credentials(Credentials, Credentials_file = 'Credentials/Credentials.pkl'):

    try:
        Credentials['Verba_Username'] and Credentials['Verba_Password']
        return Credentials
    except:
        print('No Verba Connect Credentials found. Please Enter your username and password.\n')
        Credentials['Verba_Username'] = input('Username:')
        Credentials['Verba_Password'] = input('Password:')

        # Save Verba credentials in Credentials file
        f = open(Credentials_file, 'wb')
        pickle.dump(Credentials, f)
        f.close()

    return Credentials
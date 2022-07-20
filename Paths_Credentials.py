import pickle
import os

def get(Credentials_file = 'Credentials/Credentials.pkl'):
    try:
        f = open(Credentials_file, 'rb')
        Credentials = pickle.load(f)
        f.close()
        try:
            Credentials['csv_save_path'] and Credentials['main_path']
        except:
            # Get save path
            Credentials['csv_save_path'] = input(
                'Please copy and paste the path to the folder to save the DD_update files.\nPath:').replace('\\',
                                                                                                            '/') + '/'
            Credentials['main_path'] = input(
                'Please copy and paste the path to the scripts folder.\nPath:').replace('\\', '/') + '/'
            # Save credentials file
            os.makedirs('Credentials', exist_ok=True)
            f = open(Credentials_file, 'wb')
            pickle.dump(Credentials, f)
            f.close()
        Credentials = Verba_Credentials(Credentials=Credentials)
    except:
        Credentials = {}
        # Get save path
        Credentials['csv_save_path'] = input(
            'Please copy and paste the path to the folder to save the DD_update files.\nPath:').replace('\\', '/') + '/'
        Credentials['main_path'] = input(
            'Please copy and paste the path to the scripts folder.\nPath:').replace('\\', '/') + '/'
        Credentials = Verba_Credentials(Credentials=Credentials)
        # Save credentials file
        os.makedirs('Credentials', exist_ok=True)
        f = open(Credentials_file, 'wb')
        pickle.dump(Credentials, f)
        f.close()

    return Credentials


def Verba_Credentials(Credentials, Credentials_file = 'Credentials/Credentials.pkl'):
    try:
        Credentials['Verba_Username'] and Credentials['Verba_Password']
        # if I'm running, ask for adoptions and enrolments path (containing cybersuck download folder)
        if Credentials['Verba_Username'] == 'joaquin.gonzalez':
            try:
                Credentials['adoption_enrollment_path']
            except:
                Credentials['adoption_enrollment_path'] = input(
                    'Please copy and paste the path to the adoption and enrollments folder.\nPath:').replace('\\',
                                                                                                         '/') + '/'
                # Save Verba credentials in Credentials file
                f = open(Credentials_file, 'wb')
                pickle.dump(Credentials, f)
                f.close()
    except:
        print('No Verba Connect Credentials found. Please Enter your username and password.\n')
        Credentials['Verba_Username'] = input('Username:')
        Credentials['Verba_Password'] = input('Password:')
        # if I'm running, ask for adoptions and enrolments path (containing cybersuck download folder)
        if Credentials['Verba_Username'] == 'joaquin.gonzalez':
            try:
                Credentials['adoption_enrollment_path']
            except:
                Credentials['adoption_enrollment_path'] = input(
                    'Please copy and paste the path to the adoption and enrollments folder.\nPath:').replace('\\',
                                                                                                         '/') + '/'
        # Save Verba credentials in Credentials file
        os.makedirs('Credentials', exist_ok=True)
        f = open(Credentials_file, 'wb')
        pickle.dump(Credentials, f)
        f.close()

    return Credentials
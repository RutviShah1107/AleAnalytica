import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

df = pd.read_excel('./data/kantar6k.xlsx')
# scaler = MinMaxScaler(feature_range=(-1, 1))

#### DROP NOT USED COLUMNS ##################

df.drop(columns=['Respondent_Serial', 'yyyymmdd', 'qVendor', 'qDevice', 'Gender_Quota',
                  'Age', 'qRegion_US1', 'qRegion_US2', 'qRegion_US3', 'qRegion_US4',
                  'HEthnicity', 'S0', 'State', 'Region9', 'Region4',
                  'S4', 'S51', 'S52', 'S53', 'S54', 'S55', 'S56', 'S57', 'S7'], inplace=True)

### GENERATE ETHINITY COLUMN ##############

def create_S6(row):
    S6a_values = row[['S6a1', 'S6a2', 'S6a3', 'S6a4', 'S6a5', 'S6a6']].values
    S6b_values = row[['S6b1', 'S6b2', 'S6b3', 'S6b4', 'S6b5', 'S6b6']].values

    if row['S6a1'] == 1:
        s6 = 'S6b' + str(1 + np.argmax(S6b_values))
    else:
        s6 = 'S6a'  #+ str(1 + np.argmax(S6a_values))

    return s6

df['S6'] = df.apply(create_S6, axis=1)
ethnicity_dict = {'S6b1': 1, 'S6a': 2, 'S6b2': 3, 'S6b3': 4, 'S6b4': 5, 'S6b5': 6}
df['S6'] = df['S6'].map(ethnicity_dict)
df.drop(columns=['S6b1', 'S6b2', 'S6b3', 'S6b4', 'S6b5', 'S6b6',
                 'S6a1', 'S6a2', 'S6a3', 'S6a4', 'S6a5', 'S6a6'], inplace=True)


############ SCREENER COLUMNS ######################################
# df[['HHI',	'S2',	'S3',	'S6']] = scaler.fit_transform(df[['HHI',	'S2',	'S3',	'S6']]) 

S8_columns = df.columns[df.columns.str.startswith('S8')].to_list()
df[S8_columns] = 3 - df[S8_columns]
# df[S8_columns] = scaler.fit_transform(df[S8_columns]) 

S9_columns = df.columns[df.columns.str.startswith('S9')].to_list()
df[S9_columns] = 3 - df[S9_columns]
df[S9_columns] = df[S9_columns].fillna(1)
# df[S9_columns] = scaler.fit_transform(df[S9_columns])



##### PREPROCESS ATTITUDES COLUMNS ###################

def preprocess_reverse_columns(start_str):
    columns = df.columns[df.columns.str.startswith(start_str + '_' + start_str)]

    straight_map = {1: 1, 2: 0.5, 3: -0.5, 4: -1}
    reverse_map = {1: -1, 2: -0.5, 3: 0.5, 4: 1}

    for index, row in df.iterrows():
        if row[start_str + 'Order'] == 2:
            for column in columns:
                df.loc[index, column] = reverse_map[row[column]]
        else:
            for column in columns:
                df.loc[index, column] = straight_map[row[column]]

    df.drop(columns=[start_str + 'Order'], inplace=True)  

preprocess_reverse_columns('A1')
preprocess_reverse_columns('A3')

##### PREPROCESS ATTITUDES LiKERT TYPE COLUMNS ###################

def preprocess_likert_columns(start_str):
    columns = df.columns[df.columns.str.startswith(start_str + '_')]

    map = {1: -1, 2: -0.5, 3: 0, 4: 0.5, 5: 1}

    for column in columns:
        df[column] = df[column].map(map)       

preprocess_likert_columns('A2')
preprocess_likert_columns('A4')
preprocess_likert_columns('A5')

####### ATTITUDES USING MIN MAX SCALER########################
df['A6'] = 7 - df['A6']
attitudes_columns = df.columns[df.columns.str.startswith('A8')].to_list() + df.columns[df.columns.str.startswith('A9')].to_list() + ['A6', 'A7']
df[attitudes_columns] = df[attitudes_columns].fillna(-1)
# df[attitudes_columns] = scaler.fit_transform(df[attitudes_columns]) 


######### ODD QUESTIONS ######################

ODD_columns = df.columns[df.columns.str.startswith('ODD')].to_list()
df[ODD_columns] = df[ODD_columns].fillna(-1)
# df[ODD_columns] = scaler.fit_transform(df[ODD_columns])



########## MC QUESTIONS #################
MC1_columns = df.columns[df.columns.str.startswith('MC1')].to_list()
df[MC1_columns] = 7 - df[MC1_columns]


MC6_columns = df.columns[df.columns.str.startswith('MC6')].to_list()
df[MC6_columns] = 7 - df[MC6_columns]

MC_columns = df.columns[df.columns.str.startswith('MC')].to_list()
df[MC_columns] = df[MC_columns].fillna(-1)

# df[MC6_columns + MC1_columns] = scaler.fit_transform(df[MC6_columns + MC1_columns])


############33 CLASSIFICATION ########################3

C_columns = df.columns[df.columns.str.startswith('C')].to_list()
df[C_columns] = df[C_columns].fillna(-1)
# df[C_columns] = scaler.fit_transform(df[C_columns])


####################

def filter_columns(df):
    columns_to_remove = []
    for column in df.columns:
        if round(df[column].max()) != 1 and (round(df[column].min()) != -1 or  round(df[column].min()) != 0):
          columns_to_remove.append(column)
        if df[column].isna().sum() != 0:
          columns_to_remove.append(column)
    return columns_to_remove

# columns_to_remove = filter_columns(df)

# df.drop(columns=columns_to_remove, inplace=True)

df = df.astype('float16')

df.to_csv('./data/kantar6k.csv', index=False)
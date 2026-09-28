import pytest
import pandas as pd
from sklearn.impute import SimpleImputer
from cleverminer import cleverminer

@pytest.fixture(scope="module")
def prepared_df():
    """
    Downloads and prepares the data once for all tests in this module.
    """
    url = 'https://www.cleverminer.org/data/accidents.zip'
    df = pd.read_csv(url, encoding='cp1250', sep='\t')
    
    # Filter columns
    cols = [
        'Driver_Age_Band', 'Driver_IMD', 'Sex', 'Area', 'Journey', 
        'Road_Type', 'Speed_limit', 'Light', 'Vehicle_Location', 
        'Vehicle_Type', 'Vehicle_Age', 'Hit_Objects_in', 
        'Hit_Objects_off', 'Casualties', 'Severity'
    ]
    df = df[cols]

    # Impute missing values
    imputer = SimpleImputer(strategy="most_frequent")
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    
    return df_imputed

def test_4ftminer_rule_count(prepared_df):
    """Verifies 4ftMiner procedure returns 27 rules."""
    clm = cleverminer(
        df=prepared_df, proc='4ftMiner',
        quantifiers={'Base': 20000, 'aad': 0.7},
        ante={
            'attributes': [
                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                {'name': 'Driver_IMD', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                {'name': 'Journey', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
            ], 'minlen': 1, 'maxlen': 4, 'type': 'con'
        },
        succ={
            'attributes': [
                {'name': 'Hit_Objects_in', 'type': 'rcut', 'minlen': 1, 'maxlen': 11},
                {'name': 'Hit_Objects_off', 'type': 'rcut', 'minlen': 1, 'maxlen': 11},
                {'name': 'Casualties', 'type': 'rcut', 'minlen': 1, 'maxlen': 6},
                {'name': 'Severity', 'type': 'lcut', 'minlen': 1, 'maxlen': 2}
            ], 'minlen': 1, 'maxlen': 1, 'type': 'con'
        }
    )
    assert clm.get_rulecount() == 27, f"4ftMiner failed: Expected 27 rules, but the procedure returned {clm.get_rulecount()}."

def test_sd4ftminer_rule_count(prepared_df):
    """Verifies SD4ftMiner procedure returns 10 rules."""

    clm = cleverminer(
        df=prepared_df, proc='SD4ftMiner',
        quantifiers={'Base1': 4000, 'Base2': 4000, 'Ratiopim': 1.4},
        ante={
            'attributes': [
                {'name': 'Vehicle_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                {'name': 'Speed_limit', 'type': 'seq', 'minlen': 1, 'maxlen': 2}

            ], 'minlen': 1, 'maxlen': 4, 'type': 'con'
        },
        succ={
            'attributes': [{'name': 'Severity', 'type': 'lcut', 'minlen': 1, 'maxlen': 2}],
            'minlen': 1, 'maxlen': 1, 'type': 'con'
        },
        frst={
            'attributes': [{'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 2}],
            'minlen': 1, 'maxlen': 1, 'type': 'con'
        },
        scnd={
            'attributes': [{'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 2}],
            'minlen': 1, 'maxlen': 1, 'type': 'con'
        }
    )
    assert clm.get_rulecount() == 10, f"SD4ftMiner failed: Expected 10 rules, but the procedure returned {clm.get_rulecount()}."

def test_cfminer_rule_count(prepared_df):
    """Verifies CFMiner procedure returns 9 rules."""
    clm = cleverminer(
        df=prepared_df, target='Severity', proc='CFMiner',
        quantifiers={'S_Down': 1, 'Base': 100},
        cond={
            'attributes': [
                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                {'name': 'Driver_IMD', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                {'name': 'Journey', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                {'name': 'Speed_limit', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                {'name': 'Light', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                {'name': 'Vehicle_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
            ], 'minlen': 1, 'maxlen': 2, 'type': 'con'
        }
    )
    assert clm.get_rulecount() == 9, f"CFMiner failed: Expected 9 rules, but the procedure returned {clm.get_rulecount()}."

def test_uicminer_rule_count(prepared_df):
    """Verifies UICMiner procedure returns 18 rules."""
    clm = cleverminer(
        df=prepared_df, target='Severity', proc='UICMiner',
        quantifiers={'aad_score': 20, 'aad_weights': [5, 1, 0], 'base': 200},
        ante={
            'attributes': [
                {'name': 'Driver_Age_Band', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                {'name': 'Driver_IMD', 'type': 'seq', 'minlen': 1, 'maxlen': 3},
                {'name': 'Sex', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
                {'name': 'Area', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
                {'name': 'Journey', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
                {'name': 'Road_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
                {'name': 'Speed_limit', 'type': 'seq', 'minlen': 1, 'maxlen': 2},
                {'name': 'Light', 'type': 'subset', 'minlen': 1, 'maxlen': 2},
                {'name': 'Vehicle_Type', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
            ], 'minlen': 1, 'maxlen': 2, 'type': 'con'
        }
    )
    assert clm.get_rulecount() == 18, f"UICMiner failed: Expected 18 rules, but the procedure returned {clm.get_rulecount()}."

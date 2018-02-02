"""Main script for generating output.csv."""
import pandas as pd
import numpy as np

def avg(this_df):
    return (this_df['H'] / this_df['AB']).round(3)

def obp(this_df):
    return ((this_df['H']+ this_df['BB'] + this_df['HBP']) / this_df['PA']).round(3)

def slg(this_df):
    return (this_df['TB'] / this_df['AB']).round(3)

def create_stats(this_df, style, versus, stat, hitter_bool):
    if versus == 'R':
        if hitter_bool == True:
            versus_txt = 'vs RHP'
        else:
            versus_txt = 'vs RHH'
    else:
        if hitter_bool == True:
            versus_txt = 'vs LHP'
        else:
            versus_txt = 'vs LHH'

    if stat == 'AVG':
        value = avg(this_df)
    elif stat == 'OBP':
        value = obp(this_df)
    elif stat == 'SLG':
        value = slg(this_df)
    else:
        value = slg(this_df) + obp(this_df)
        
    e = pd.DataFrame({'SubjectId' : this_df.index, 'Stat' : stat, 'Subject' : style, 'Split' : versus_txt, 'Value' : value},
                    columns=['SubjectId', 'Stat', 'Split', 'Subject', 'Value'])
    e = e.reset_index(drop = True)
    return e

def main():
    df = pd.read_csv('./data/raw/pitchdata.csv')
    total = pd.DataFrame(columns=['SubjectId', 'Stat', 'Split', 'Subject', 'Value'])
    for style in ['HitterId', 'HitterTeamId', 'PitcherId', 'PitcherTeamId']:
        for versus in ['R', 'L']:
            if 'Hitter' in style:
                sums = df[df.PitcherSide == versus].groupby(style).sum()
                hitter_bool = True
            else:
                sums = df[df.HitterSide == versus].groupby(style).sum()
                hitter_bool = False
            sums_filtered = sums[sums.PA >= 25]
            for stat in ['AVG', 'OBP', 'SLG', 'OPS']:
                stats_df = create_stats(sums_filtered, style, versus, stat, hitter_bool)
                total = total.append(stats_df)
    total = total.sort(['SubjectId', 'Stat', 'Split', 'Subject'])
    total.to_csv('./data/processed/output2.csv', index = False)
    pass


if __name__ == '__main__':
    main()

#'''
import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV with Modality as index
df = pd.read_csv("Timing.csv", sep=';')

df['Difference_MS'] = pd.to_numeric(df['Difference_MS'].str.replace(',', '.'), errors='coerce')

#df['Difference_MS'] = df['Difference_MS'].apply(lambda x: '{:.3f}'.format(x) if pd.notnull(x) else x)

# Transpose DataFrame to have Modality as columns

# Plot individual plots for each modality
difference_types = ['Frames', 'MS']
for x in range(2):
    difference_type = difference_types[x]
    for modality in df['Modality'].unique():
        plt.figure(figsize=(8, 6))
        modality_data = df[df['Modality'] == modality]
        duration_counts = modality_data['Difference_' + difference_type].value_counts().sort_index()
        plt.bar(duration_counts.index.astype(str), duration_counts.values)
        #plt.bar(duration_counts.index, duration_counts.values)
        plt.title(f'Count of Items by Duration ({difference_type}) for {modality}')
        plt.xlabel(f'Duration ({difference_type})')
        plt.ylabel('Amount of occurences')
        plt.xticks(rotation=45, ha='right')
        plt.grid(False)
        plt.tight_layout()
        plt.savefig('pictures/'+modality + '_' + difference_type +'.png')

'''
import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV with Modality as index
df = pd.read_csv("Timing.csv", sep=';')

# Plot individual plots for each modality
for modality in df['Modality'].unique():
    plt.figure(figsize=(8, 6))
    modality_data = df[df['Modality'] == modality]
    duration_counts = modality_data['Difference_MS'].value_counts().sort_index()
    plt.bar(duration_counts.index.astype(str), duration_counts.values)
    plt.title(f'Count of Items by Duration (MS) for {modality}')
    plt.xlabel('Duration (MS)')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
#'''

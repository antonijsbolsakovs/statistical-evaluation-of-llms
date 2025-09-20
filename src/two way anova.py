import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import shapiro
# folders
#anova analysis of prompt categories and model versions

# folders
# proportions2.0
# proportions1.5 

# csv files
# CREATIVE PROMPTS_x.x_proportions.csv
# FAQ_x.x_proportions.csv
# MULTIPLE_x.x_proportions.csv
# NON_x.x_proportions.csv
# RIDDLES_x.x_proportions.csv
# STEM_x.x_proportions.csv

resulting_tables = []

# Define prompt types and versions
prompt_types = ['CREATIVE PROMPTS', 'FAQ', 'MULTIPLE', 'NON', 'RIDDLES', 'STEM']
versions = {'1.5': 'proportions1.5', '2.0': 'proportions2.0'}

# Helper to build file paths
def build_path(version, prompt):
    prompt_file = f"{prompt}_{version}_proportions.csv"
    return f"{versions[version]}/{prompt_file}"

# Load datasets into dictionaries
datasets = {}
for version in versions:
    datasets[version] = {}
    for prompt in prompt_types:
        path = build_path(version, prompt)
        df = pd.read_csv(path, sep=',')
        # Drop specified columns if they exist
        cols_to_drop = ['filename', 'total_words', 'english_only', 'danish_only', 'ambiguous', 'neither']
        df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)
        # Use simplified prompt name as key
        key = prompt.split()[0].capitalize() if prompt != 'CREATIVE PROMPTS' else 'Creative'
        datasets[version][key] = df

datasets15 = datasets['1.5']
datasets20 = datasets['2.0']

print("Datasets loaded successfully.")


combined_data = []

for version, prompt_dict in datasets.items():
    for prompt_type, df in prompt_dict.items():
        for _, row in df.iterrows():
            combined_data.append({
                'llm_version': version,
                'prompt_type': prompt_type,
                'prop_english_only': row['prop_english_only']  # adjust this if you want a different measure
            })

anova_df = pd.DataFrame(combined_data)
# anova_df.to_csv('anova_combined_data.csv', index=False)

# anova_df["log_prop_english_only"] = np.log(anova_df['prop_english_only'] + 1e-10)  # Adding a small constant to avoid log(0)



# Drop rows with missing values in relevant columns
anova_df = anova_df.dropna(subset=['prop_english_only'])
# Relevant coloumns: prop_english_only,prop_danish_only,prop_ambiguous,prop_neither
# Convert factors to categorical 
anova_df['llm_version'] = anova_df['llm_version'].astype('category')
anova_df['prompt_type'] = anova_df['prompt_type'].astype('category')

# Run two-way ANOVA with interaction
model = ols('prop_english_only ~ C(llm_version) + C(prompt_type) + C(llm_version):C(prompt_type)', data=anova_df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

print(anova_table)


sns.pointplot(data=anova_df, x="prompt_type", y="prop_english_only", hue="llm_version", dodge=True)
plt.xticks(rotation=45)
plt.title("Interaction between prompt type and LLM version")
plt.show()

# Plot residuals of the ANOVA model
residuals = model.resid
fitted = model.fittedvalues

plt.figure(figsize=(8, 5))
sns.residplot(x=fitted, y=residuals, lowess=True, line_kws={'color': 'red', 'lw': 1})
plt.xlabel("Fitted values")
plt.ylabel("Residuals")
plt.title("Residuals vs Fitted Values")
plt.tight_layout()
plt.show()

# QQ plot for normality of residuals
sm.qqplot(residuals, line='s')
plt.title("QQ Plot of Residuals")
plt.tight_layout()
plt.show()


# Check normality of residuals: Shapiro-Wilk test

shapiro_stat, shapiro_p = shapiro(residuals)
print(f"Shapiro-Wilk test statistic: {shapiro_stat:.4f}, p-value: {shapiro_p:.4g}")
if shapiro_p > 0.05:
    print("Residuals are approximately normal (fail to reject H0).")
else:
    print("Residuals are not normal (reject H0).")



# plt.figure(figsize=(10, 6))
# sns.boxplot(x='prompt_type', y='prop_english_only', hue='llm_version', data=anova_df)
# plt.title('English-Only Proportion by Prompt Type and LLM Version')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()



# # Drop missing
# anova_df = anova_df.dropna(subset=['prop_english_only'])

# # Ensure string types
# anova_df['prompt_type'] = anova_df['prompt_type'].astype(str)
# anova_df['llm_version'] = anova_df['llm_version'].astype(str)

# # Create interaction group
# anova_df['interaction_group'] = (
#     anova_df['prompt_type'] + "_" + anova_df['llm_version']
# )

# # Tukey post hoc
# from statsmodels.stats.multicomp import pairwise_tukeyhsd

# tukey_result = pairwise_tukeyhsd(
#     endog=anova_df['prop_english_only'],
#     groups=anova_df['interaction_group'],
#     alpha=0.05
# )

# print(tukey_result.summary())


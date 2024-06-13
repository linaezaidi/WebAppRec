#Traitement et analyse RFM 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#CHARGEMENT DU DATASET 
shirts_df = pd.read_csv('DATA/shirts.csv')
purchases_df = pd.read_csv('DATA/purchases.csv')
users_df = pd.read_csv('DATA/users.csv')

# Convertir la colonne date en datetime
purchases_df['date'] = pd.to_datetime(purchases_df['date'])

# Calculer la quantité totale vendue pour chaque t-shirt
total_sold = purchases_df.groupby('id')['quantity'].sum().reset_index()

# Fusionner avec les données des t-shirts pour obtenir les détails des t-shirts
most_sold_shirts = total_sold.merge(shirts_df, left_on='id', right_on='id')

# Trier par quantité vendue en ordre décroissant
most_sold_shirts = most_sold_shirts.sort_values(by='quantity', ascending=False)

# Afficher les 10 t-shirts les plus vendus
print("Top 10 des t-shirts les plus vendus :")
print(most_sold_shirts.head(10))

# Fonction pour obtenir des recommandations basées sur les t-shirts les plus vendus
def get_recommendations(top_n=10):
    return most_sold_shirts.head(top_n)

# Utilisation
recommendations = get_recommendations()
print("\nT-shirts recommandés :")
print(recommendations[['team', 'image', 'price', 'quantity']])

# Tracer les 10 t-shirts les plus vendus
plt.figure(figsize=(12, 8))
sns.barplot(data=most_sold_shirts.head(10), x='quantity', y='team', hue='team', palette='viridis', dodge=False, legend=False)
plt.xlabel('Quantité Vendue')
plt.ylabel('Équipe')
plt.title('Top 10 des T-shirts les Plus Vendus')
plt.savefig('top_10_most_sold_shirts.png')
plt.close()

# Analyse RFM
# RFM : Récence, Fréquence, Valeur Monétaire
# Récence : jours depuis le dernier achat
# Fréquence : nombre d'achats
# Monétaire : montant total dépensé

# Récence
max_date = purchases_df['date'].max()
rfm = purchases_df.groupby('uid').agg({
    'date': lambda x: (max_date - x.max()).days,
    'id': 'count',
    'quantity': 'sum'
}).reset_index()

rfm.columns = ['uid', 'recency', 'frequency', 'monetary']

# Fusionner RFM avec les données des utilisateurs
rfm = rfm.merge(users_df, left_on='uid', right_on='id')

# Tracer les distributions RFM et sauvegarder les images
plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
sns.histplot(rfm['recency'], bins=20, kde=True, color='blue')
plt.title('Distribution de la Récence')
plt.savefig('rfm_recency_distribution.png')

plt.subplot(1, 3, 2)
sns.histplot(rfm['frequency'], bins=20, kde=True, color='green')
plt.title('Distribution de la Fréquence')
plt.savefig('rfm_frequency_distribution.png')

plt.subplot(1, 3, 3)
sns.histplot(rfm['monetary'], bins=20, kde=True, color='red')
plt.title('Distribution de la Valeur Monétaire')
plt.savefig('rfm_monetary_distribution.png')

plt.show()
plt.close()

# Afficher les meilleurs segments RFM
rfm['RFM_Score'] = rfm['recency'].rank(ascending=False) + rfm['frequency'].rank(ascending=True) + rfm['monetary'].rank(ascending=True)
top_rfm_segments = rfm.sort_values('RFM_Score').head(10)
print("Meilleurs segments RFM :")
print(top_rfm_segments[['username', 'recency', 'frequency', 'monetary', 'RFM_Score']])

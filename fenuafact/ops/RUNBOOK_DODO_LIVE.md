# Passage de Dodo Payments en mode Live

> Prérequis : compte vérifié (WaveFi encaisse déjà en réel), marque FenuaFact existante.
> Les environnements test et live sont **séparés** : produits, clés et webhooks doivent être recréés.

## 1. Recréer les produits en Live

Dashboard Dodo → basculer en **Mode réel** → Produits.
Ouvrir chaque produit de test et utiliser **« Copier vers le mode réel »** (ou recréer à l'identique) :

| Nom | Prix | Période | Marque |
| --- | --- | --- | --- |
| FenuaFact Essentiel | 7 950 XPF | mensuel | FenuaFact |
| FenuaFact Pro | 12 900 XPF | mensuel | FenuaFact |

Noter les deux nouveaux `product_id` (ils diffèrent de ceux de test).

## 2. Créer la clé API Live

Développeur → API Keys → **Créer** (en mode réel) :
- Nom : `fenuafact-server-live`
- Sessions de checkout → Écriture · Produits, Abonnements, Clients → Lecture · reste Aucun
- IP Allowlist : `194.163.44.206`
- Préfixe attendu : **`dodo_live_`**

## 3. Créer le webhook Live

Développeur → Webhooks → Ajouter un point de terminaison (en mode réel) :
- URL : `https://api.fenuafact.com/webhooks/dodo`
- Événements : laisser vide (tous)
- Noter le secret `whsec_…` (propre au mode réel)

> L'endpoint de test reste en place : ne pas le supprimer.

## 4. Basculer l'environnement du serveur

```bash
cd /var/www/fenuafact-api
cp -a .env .env.test          # sauvegarde pour revenir en test
nano .env
```

Remplacer :

```ini
DODO_API_KEY=dodo_live_...
DODO_WEBHOOK_SECRET=whsec_...       # celui du webhook LIVE
DODO_PRODUCT_ESSENTIEL=pdt_...      # produit live
DODO_PRODUCT_PRO=pdt_...            # produit live
DODO_BASE_URL=https://live.dodopayments.com
```

```bash
systemctl restart fenuafact
sleep 5
curl -s https://api.fenuafact.com/health
```

## 5. Vérifier la clé live

```bash
KEY=$(grep '^DODO_API_KEY=' .env | cut -d= -f2-)
curl -s -H "Authorization: Bearer $KEY" https://live.dodopayments.com/products
```

Les deux produits FenuaFact doivent apparaître.

## 6. Test réel (obligatoire)

1. Depuis le front, cliquer « Choisir cette offre » sur Essentiel
2. Payer **7 950 XPF** avec une vraie carte
3. Vérifier : `tenants.abonnement_statut = actif`, `/abonnement` affiche la bonne offre
4. **Rembourser immédiatement** depuis le dashboard Dodo
5. Annuler l'abonnement de test réel

Coût : les frais Dodo (~8 %), soit ~600 XPF. C'est le prix de la certitude.

## 7. Retour arrière

```bash
cd /var/www/fenuafact-api
cp -a .env.test .env
systemctl restart fenuafact
```

## Points de vigilance

- Ne jamais créer un abonnement live pour la démo : il sera prélevé chaque mois.
- Le compte de démonstration (`tenant 1111…`) est en Pro **manuel** : avant une démo, vérifier qu'aucun abonnement live ne le remplace.
- Conserver `.env.test` aussi longtemps que le mode test sert au développement.

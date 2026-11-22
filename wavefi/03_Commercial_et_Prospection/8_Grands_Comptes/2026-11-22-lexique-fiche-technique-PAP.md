# Lexique de la fiche technique PAP

> Rédigé le **2026-11-22**. Document **interne**.
> Vocabulaire employé dans `2026-11-19-fiche-technique-PAP.md`, expliqué en français courant.
>
> ⚠️ **Ne jamais joindre ce lexique au Port.** Un service informatique connaît ces mots par cœur ;
> le lui envoyer serait condescendant, et donnerait le signal inverse de celui recherché. Cette
> feuille est pour toi, avant et après la réunion.

| Terme | En une phrase | Ce que tu réponds |
|---|---|---|
| **Overlay** | Couche logicielle par-dessus l'existant | « On ne remplace ni vos bornes ni votre contrôleur. » |
| **SSID** | Nom du réseau Wi-Fi visible | « Le réseau invité que vos passagers voient. » |
| **Borne / AP** | L'antenne qui diffuse le Wi-Fi | « Vos bornes restent en place. » |
| **Contrôleur** | Le cerveau qui pilote les bornes | « C'est chez vous, on s'y branche. » |
| **RADIUS** | Répond oui ou non à une connexion | « Notre serveur d'authentification. » |
| **UDP** | Transport rapide, sans accusé de réception | « Le standard pour le RADIUS. » |
| **Ports 1812 / 1813** | Authentification et comptabilité RADIUS | « Deux ports UDP à autoriser en sortie. » |
| **DHCP** | Distribue les adresses IP | « Le vôtre reste en place. » |
| **DNS** | Traduit les noms de domaine | « Sans lui, le portail ne charge pas. » |
| **VLAN** | Réseau séparé dans le réseau physique | « L'invité ne voit pas votre exploitation. » |
| **HTTPS / TLS** | Chiffrement des échanges | « Le portail est chiffré. » |
| **Wi-Fi 6** | Génération récente du Wi-Fi | « Vos bornes sont à jour. » |
| **Portail captif** | Page affichée avant l'accès internet | « C'est la page aux couleurs du Port. » |
| **Walled garden** | Sites joignables avant authentification | « À configurer chez vous, on donne la liste. » |
| **Consentement** | Accord explicite du passager | « Deux cases, aucune pré-cochée. » |
| **Agrégé** | Statistiques de groupe, pas de personnes | « On dit combien, pas qui. » |
| **Sous-traitant** | Traite des données pour un autre | « Vous responsable, nous sous-traitant. » |
| **DPA** | Contrat encadrant les données | « L'annexe est au dossier. » |
| **SLA** | Engagement de service | « Il se construit avec vous. » |
| **Supervision** | Surveillance automatique avec alerte | « Contrôle quotidien, alerte si panne. » |
| **Recette** | Validation finale par le client | « Vous signez, sur dix vérifications. » |
| **Cloud** | Hébergé chez un prestataire | « Chez nous, hors de votre réseau. » |
| **API** | Porte d'entrée entre deux logiciels | « Nos échanges avec vos outils. » |

## Les trois mots à connaître par cœur

**SSID**, **RADIUS**, **walled garden**. Ce sont ceux qui reviendront dans la conversation, et ceux
qui prouvent que tu sais de quoi tu parles. Le reste, tu peux l'apprendre en réunion — un DSI ne
juge pas ta vitesse, il juge ta rigueur.

## Et trois tournures qui valent mieux que le jargon

| Au lieu de | Dis |
|---|---|
| « Il faut ouvrir les ports 1812 et 1813 en UDP sortant » | « Il faut autoriser votre contrôleur à joindre notre serveur d'authentification. » |
| « Le walled garden doit inclure app.wavefi.tech » | « Avant connexion, il faut laisser passer l'adresse de notre page. » |
| « Le VLAN invité doit être isolé » | « Le réseau invité doit rester séparé de votre réseau d'exploitation. » |

Tu peux nommer les ports et les protocoles **après** avoir dit la phrase simple — jamais avant.

# Lexique de la fiche technique PAP

> Rédigé le **2026-11-22**. Document **interne**.
> Vocabulaire employé dans `2026-11-19-fiche-technique-PAP.md`, expliqué en français courant.
>
> ⚠️ **Ne jamais joindre ce lexique au Port.** Un service informatique connaît ces mots par cœur ;
> le lui envoyer serait condescendant, et donnerait le signal inverse de celui recherché. Cette
> feuille est pour toi, avant et après la réunion.

| Terme | En une phrase | Ce que tu réponds si on te demande |
|---|---|---|
| **Overlay** | Une couche logicielle posée **par-dessus** une installation existante, sans la remplacer | « On ne touche ni à vos bornes ni à votre contrôleur : on ajoute la page d'accueil. » |
| **SSID** | Le nom du réseau Wi-Fi visible par le client (`GUEST_TCI`) | « C'est le réseau invité que vos passagers voient déjà. » |
| **Borne / AP** | L'antenne qui diffuse le Wi-Fi dans une zone | « Vos bornes restent en place, ce sont des Alcatel-Lucent. » |
| **Contrôleur** | Le cerveau qui pilote les bornes et porte les règles du réseau | « C'est chez vous, on s'y branche. » |
| **RADIUS** | Le service qui répond oui ou non à une demande de connexion | « C'est notre serveur d'authentification. » |
| **UDP** | Protocole de transport rapide, sans accusé de réception | « Le RADIUS utilise UDP, c'est le standard. » |
| **Port 1812 / 1813** | Les deux « portes » du RADIUS : authentification et comptabilité | « Deux ports UDP à autoriser en sortie vers notre serveur. » |
| **DHCP** | Le service qui distribue les adresses IP aux appareils | « Le vôtre reste en place, on n'y touche pas. » |
| **DNS** | Le service qui traduit les noms de domaine en adresses | « Sans lui, le portail ne se charge pas. » |
| **VLAN** | Un réseau séparé à l'intérieur du réseau physique | « L'invité ne voit jamais votre réseau d'exploitation. » |
| **HTTPS / TLS** | Le chiffrement des échanges entre le navigateur et le portail | « Le portail est chiffré, comme n'importe quel site sérieux. » |
| **Wi-Fi 6 / 802.11ax** | La génération récente du Wi-Fi | « Vos bornes sont en Wi-Fi 6 : le matériel est à jour. » |
| **Portail captif** | La page qui s'affiche avant d'accorder l'accès internet | « C'est la page aux couleurs du Port. » |
| **Walled garden** | La liste des sites joignables **avant** d'être authentifié | « Ça se configure chez vous, on vous donne la liste. » |
| **Consentement** | L'accord explicite du passager avant toute collecte | « Deux cases distinctes, aucune pré-cochée. » |
| **Agrégé / anonymisé** | Des statistiques de groupe, jamais des personnes | « On dit combien de passagers, pas qui. » |
| **Sous-traitant** | L'entreprise qui traite des données pour le compte d'une autre | « Vous êtes responsable, nous sommes sous-traitant. » |
| **DPA** | Le contrat qui encadre le traitement des données | « L'annexe de traitement des données est au dossier. » |
| **SLA** | L'engagement de niveau de service : disponibilité, délais | « Il n'existe pas encore — il se construit avec vous. » |
| **Supervision** | La surveillance automatique d'un service, avec alerte | « Un contrôle quotidien, avec alerte si le portail ne répond plus. » |
| **Recette** | La validation finale, faite par le client, avant mise en service | « C'est vous qui signez la recette, sur dix vérifications. » |
| **Cloud** | Un service hébergé chez un prestataire, pas dans vos murs | « Hébergé chez nous, hors de votre réseau. » |
| **API** | Une porte d'entrée technique entre deux logiciels | « Nos échanges avec vos outils passent par des API. » |

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

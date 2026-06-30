# L'obligation de sécurité des données : ce que la sanction CNIL contre Free et Free Mobile enseigne sur l'article 32 du RGPD

Le 8 janvier 2026, la formation restreinte de la Commission nationale de l'informatique et des libertés — l'organe de la CNIL chargé de prononcer les sanctions — a rendu deux décisions retentissantes contre deux opérateurs de télécommunications du groupe Iliad : la société Free Mobile et la société Free. Publiées le 13 janvier 2026, ces délibérations, numérotées SAN-2026-001 et SAN-2026-002, prononcent respectivement des amendes de vingt-sept millions et de quinze millions d'euros, soit un total de quarante-deux millions d'euros. Au-delà du montant, qui figure parmi les plus élevés jamais infligés par l'autorité française, cette affaire offre un cas d'école pour comprendre une obligation centrale du droit de la protection des données : l'obligation de sécurité posée par l'article 32 du règlement général sur la protection des données, le RGPD.

## Le contexte : une intrusion et une fuite massive

Tout commence en octobre 2024. Un attaquant parvient à s'infiltrer dans le système d'information des deux sociétés et à accéder à des données personnelles concernant vingt-quatre millions de contrats d'abonnés. Parmi ces données figurent, pour les personnes qui étaient à la fois clientes de Free Mobile et de Free, des coordonnées bancaires sous forme d'IBAN — une donnée particulièrement sensible, car elle peut servir à des opérations frauduleuses telles que des prélèvements non autorisés ou des tentatives d'hameçonnage ciblé. À la suite de cette violation, la CNIL reçoit un très grand nombre de plaintes, plus de deux mille cinq cents, émanant de personnes concernées. Cet afflux déclenche un contrôle, qui met en évidence des manquements à plusieurs obligations du RGPD, imputables à chacune des deux sociétés en tant que responsable du traitement des données de ses propres abonnés.

Il faut insister sur un point souvent mal compris : la CNIL ne sanctionne pas ici le fait d'avoir été piraté. Une cyberattaque, en elle-même, n'est pas une faute. Ce que l'autorité reproche, c'est l'insuffisance des mesures de sécurité qui, si elles avaient été en place, auraient rendu l'attaque plus difficile, voire l'auraient empêchée ou en auraient limité les conséquences. C'est exactement la logique de l'article 32.

## L'article 32 du RGPD : une obligation de moyens adaptée au risque

L'article 32 du RGPD impose au responsable du traitement et à son sous-traitant de mettre en œuvre les mesures techniques et organisationnelles appropriées afin de garantir un niveau de sécurité adapté au risque. Le texte ne dresse pas une liste fermée de mesures obligatoires : il raisonne par le risque. Plus les données sont nombreuses, sensibles, ou susceptibles de causer un préjudice en cas de fuite, plus le niveau de sécurité attendu est élevé. L'article cite néanmoins des exemples — la pseudonymisation, le chiffrement, la capacité à garantir la confidentialité, l'intégrité, la disponibilité et la résilience des systèmes, ainsi que des procédures de test et d'évaluation régulières de l'efficacité des mesures.

C'est donc une obligation de moyens, mais une obligation de moyens renforcée : elle s'apprécie concrètement, au regard de l'état de l'art, des coûts de mise en œuvre, et de la nature des données traitées. Dans le cas de Free et Free Mobile, la formation restreinte a estimé que, compte tenu du nombre et de la nature des données — vingt-quatre millions de contrats, des IBAN —, le niveau de sécurité déployé n'était pas adapté.

## Les défaillances précises relevées

La décision est instructive parce qu'elle nomme des défaillances très concrètes, immédiatement parlantes pour quiconque travaille en sécurité informatique. Deux points ressortent.

Premièrement, la procédure d'authentification permettant de se connecter aux réseaux privés virtuels — les VPN — des deux sociétés n'était pas suffisamment robuste. Ces VPN étaient notamment utilisés pour le travail à distance des employés. Or un accès distant mal protégé constitue une porte d'entrée privilégiée pour un attaquant : si l'authentification repose sur un simple identifiant et mot de passe, sans deuxième facteur solide, un identifiant compromis suffit à pénétrer le réseau interne. La CNIL pointe ici, en creux, l'absence ou la faiblesse d'une authentification multifacteur sur les accès privilégiés.

Deuxièmement, les mesures déployées pour détecter les comportements anormaux sur le système d'information étaient inefficaces. Autrement dit, la capacité de détection — journalisation, supervision, corrélation d'événements, alertes — ne permettait pas de repérer à temps l'activité malveillante. La CNIL a d'ailleurs publié par le passé une recommandation dédiée aux mesures de journalisation, signe qu'elle considère cette capacité comme un élément structurant de la sécurité.

La formation restreinte a rappelé un principe fondamental : il est impossible d'éliminer tout risque, mais des mesures appropriées peuvent en réduire la probabilité et, le cas échéant, en limiter la gravité. C'est précisément cette réduction du risque que les sociétés n'avaient pas suffisamment assurée.

## Deux autres manquements : information et conservation

L'affaire ne se limite pas à l'article 32. La CNIL retient aussi un manquement à l'article 34 du RGPD, qui impose de communiquer la violation aux personnes concernées lorsqu'elle est susceptible d'engendrer un risque élevé pour leurs droits et libertés. Les sociétés avaient bien informé leurs abonnés, par un courriel puis par un numéro vert, mais la formation restreinte a jugé que le courriel ne contenait pas toutes les informations exigées par l'article 34 : il ne permettait pas aux personnes de comprendre directement les conséquences de la violation ni les mesures qu'elles pouvaient prendre pour se protéger.

Enfin, à l'encontre de Free Mobile seule, la CNIL retient un manquement à l'article 5-1-e), le principe de limitation de la durée de conservation. La société conservait, sans justification, les données de millions d'anciens abonnés pendant une durée excessive, sans tri permettant de ne garder que ce qui était nécessaire à des fins comptables. La CNIL a enjoint à la société de finaliser le tri et la purge de ces données dans un délai de six mois.

## Les enjeux pour un professionnel de la sécurité

Cette décision est une grille de lecture précieuse. Elle confirme que les fondamentaux de l'hygiène de sécurité — authentification multifacteur sur les accès distants et privilégiés, journalisation, détection et réponse aux anomalies — ne relèvent pas seulement des bonnes pratiques techniques, mais constituent désormais un socle juridiquement exigible, dont le défaut se chiffre en dizaines de millions d'euros. Elle illustre aussi le lien étroit entre sécurité et minimisation : conserver des données au-delà du nécessaire élargit la surface d'attaque et aggrave l'ampleur d'une fuite. Une donnée supprimée à l'échéance de sa durée de conservation est une donnée qui ne peut pas être volée.

Pour un architecte ou un consultant en sécurité offensive, l'affaire fournit un argumentaire concret pour justifier des investissements : MFA, supervision, gestion du cycle de vie des données. La conformité à l'article 32 ne se démontre pas par une simple déclaration, mais par des mesures effectives, testées, proportionnées au risque, et documentées. La sanction de Free et Free Mobile rappelle qu'en matière de sécurité des données personnelles, le droit français et européen attend désormais des résultats vérifiables, pas des intentions.

## Références

- CNIL, « Violation de données : sanction de 42 millions d'euros à l'encontre des sociétés FREE MOBILE et FREE », 14 janvier 2026 : https://www.cnil.fr/fr/sanction-free-2026
- Délibération de la formation restreinte SAN-2026-001 du 8 janvier 2026 (Free Mobile), Légifrance : https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000053352664
- Délibération de la formation restreinte SAN-2026-002 du 8 janvier 2026 (Free), Légifrance : https://www.legifrance.gouv.fr/cnil/id/CNILTEXT000053352643
- Article 32 du RGPD (sécurité du traitement) : https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4#Article32

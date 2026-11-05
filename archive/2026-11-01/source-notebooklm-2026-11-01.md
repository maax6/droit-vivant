# Digital Omnibus : la position du Conseil de l'UE sur le RGPD, les cookies et le signalement d'incidents (21 octobre 2026)

Ce document est une source pédagogique autonome. Il décrit une étape législative récente et le dit clairement : il s'agit de la position de négociation des États membres, et non d'une loi en vigueur. Les détails ont été recoupés sur plusieurs comptes rendus de la presse juridique ; la page du communiqué officiel du Conseil n'a pas pu être ouverte directement, et tout point précis doit donc être vérifié dans le texte du Conseil avant d'être utilisé.

## Le contexte : qu'est-ce que le Digital Omnibus ?

À l'automne 2025, la Commission européenne a présenté une série de textes de « simplification » du corpus numérique européen, regroupés sous l'étiquette Digital Omnibus. Il y a deux branches. La première, consacrée à l'IA, a déjà abouti : le règlement (UE) 2026/1744, entré en vigueur le 27 juillet 2026, a reporté les obligations applicables aux systèmes à haut risque et ajouté une interdiction à l'article 5 de l'AI Act. Ce module-ci porte sur la seconde branche, dite « données » (procédure 2025/0360(COD)), qui touche le RGPD, la directive ePrivacy 2002/58/CE, le règlement sur les données et la directive NIS2 sur la cybersécurité.

La procédure est celle de la codécision. La Commission propose. Le Conseil, qui réunit les gouvernements, arrête sa position. Le Parlement européen arrête la sienne. Ensuite seulement, les deux institutions négocient en trilogue un texte commun, qui doit être adopté formellement par chacune. Le 21 octobre 2026, le Conseil a franchi sa propre étape. Le Parlement n'a pas encore fixé la sienne. Un cabinet d'avocats indique que les négociations entre institutions ne sont pas attendues avant mars 2027, et le Conseil évoque une volonté de boucler les paquets de simplification d'ici la fin de 2027. Ces calendriers sont indicatifs.

## Ce que le Conseil a retenu

### La définition de la donnée personnelle reste la même

L'article 4, point 1, du RGPD définit la donnée à caractère personnel comme toute information se rapportant à une personne physique identifiée ou identifiable. La Commission proposait de modifier cette définition, ce qui aurait pu faire sortir certaines données du champ du RGPD selon la capacité de chaque destinataire à identifier la personne. Le Comité européen de la protection des données et le Contrôleur européen de la protection des données avaient, dans un avis conjoint de février 2026, fortement déconseillé cette modification. Le Conseil a suivi cette ligne : il conserve la définition actuelle.

Il ajoute en revanche une disposition sur la pseudonymisation, présentée comme un nouvel article 25 bis. Le principe rapporté est que des données pseudonymisées ne sont pas des données personnelles pour un tiers qui ne peut pas identifier la personne, mais le restent pour un destinataire qui le peut. Le CEPD devrait émettre un avis sur les frontières entre pseudonymisation et anonymisation. Pour un chercheur en sécurité, c'est une question très concrète : un jeu de données hachées ou tokenisées est-il une donnée personnelle ? La réponse dépend de qui le détient et de ce qu'il peut recouper.

### L'IA et l'intérêt légitime : une lecture disputée

L'article 6, paragraphe 1, point f), du RGPD autorise un traitement fondé sur l'intérêt légitime du responsable, sous réserve que les droits et libertés de la personne ne prévalent pas. La Commission voulait expliciter que cette base peut servir à développer et exploiter des systèmes d'IA. Les comptes rendus du texte du Conseil divergent. Selon l'un, le Conseil a supprimé la modification et ajouté un considérant disant que développer ou exploiter une IA n'est pas en soi un intérêt légitime, à apprécier au cas par cas. Selon un autre, le texte introduirait un article 88 bis permettant ce traitement avec des garanties techniques et organisationnelles, tout en reportant la minimisation des données dans un considérant. L'association noyb, qui a réagi le 23 octobre, parle d'« expropriation numérique » et soutient que le texte rend automatiquement licite le traitement « dans le contexte de l'IA ». Le même compte rendu note que le considérant du Conseil dit l'inverse. La seule conclusion sûre est donc négative : on ne peut pas résumer ce point en une phrase sans lire le texte du Conseil. Le traitement de catégories particulières de données pour développer l'IA serait par ailleurs limité aux données résiduelles et accessoires dont la suppression est techniquement impossible ou disproportionnée, et l'exemption pour la vérification biométrique serait limitée aux comparaisons un-à-un.

### Les cookies : plus d'exceptions, moins de bannières

La règle de base de l'article 5, paragraphe 3, de la directive ePrivacy est que lire ou écrire une information sur le terminal d'un utilisateur exige son consentement, sauf exception étroite. C'est le fondement de nombreuses sanctions de la CNIL, y compris celle contre Fnac Darty traitée dans ce dépôt le 30 octobre 2026. Le Conseil maintient les règles dans la directive ePrivacy plutôt que de les transférer au RGPD, et élargit les cas sans consentement : mesure d'audience agrégée, sécurité, fourniture du service, et mesure de l'affichage et de la performance de la publicité contextuelle sans données personnelles. Le délai avant de pouvoir redemander un consentement refusé serait de quatre mois, contre six dans la proposition de la Commission. L'exigence d'un signal de consentement lisible par machine serait remplacée par l'obligation de permettre un refus en un clic ou équivalent.

### Violations de données et signalement d'incidents

Le RGPD impose de notifier une violation à l'autorité dans les 72 heures lorsqu'elle présente un risque (article 33), et d'informer les personnes lorsque le risque est élevé (article 34). Le Conseil conserve l'idée de ne pas notifier les violations qui ne présentent pas de risque élevé, soutient un allongement du délai (le chiffre exact est à vérifier dans le texte), et prévoit une liste européenne des traitements susceptibles de présenter un risque élevé ainsi que des modèles de notification communs. Le CEPD devrait établir les circonstances où un risque élevé est probable ou non.

Pour NIS2 (directive 2022/2555, article 23), la Commission proposait un point d'entrée unique européen pour déclarer les incidents. Le Conseil le remplace par des points d'entrée nationaux dans chaque État membre, avec un point d'information européen tenu par l'ENISA et un cadre harmonisé de notification, y compris transfrontalier.

## Pourquoi cela compte pour la pratique

Trois conséquences concrètes se dégagent, toutes conditionnelles puisque le texte est un mandat. D'abord, la cartographie des traceurs d'une application ou d'un site deviendrait un exercice plus fin : certains traceurs de mesure ou de sécurité sortiraient du champ du consentement, mais pas ceux qui servent à personnaliser ou à entraîner un modèle de recommandation. Ensuite, le statut des données pseudonymisées deviendrait relatif au destinataire, ce qui oblige à documenter qui peut ré-identifier quoi. Enfin, l'architecture des déclarations d'incidents dépendrait du guichet national, ce qui compliquerait l'automatisation d'une notification multi-pays.

## Ce qui n'est pas acquis

Il n'y a aucune obligation nouvelle en vigueur. Le Parlement peut s'écarter du Conseil, en particulier sur l'IA et les cookies, où les positions divergent. Les chiffres et formulations ci-dessus proviennent de comptes rendus secondaires, et il convient de les confronter au communiqué du Conseil du 21 octobre 2026 et au texte du mandat.

## Références

- Procédure 2025/0360(COD), Digital Omnibus, volet données.
- Règlement (UE) 2016/679 (RGPD), articles 4 point 1, 6 § 1 f), 33 et 34.
- Directive 2002/58/CE (ePrivacy), article 5 § 3.
- Directive (UE) 2022/2555 (NIS2), article 23.
- Communiqué du Conseil de l'UE du 21 octobre 2026, relevé via Lovguiden, et analyses d'Addleshaw Goddard et d'Anoni.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez l'angle qui correspond à votre usage et collez-le tel quel dans le champ de personnalisation.

**Angle 1 — Audit offensif des traceurs.** Concentre-toi sur ce que les nouvelles exceptions de consentement changeraient pour un audit technique d'application mobile ou de site : quels traceurs et API resteraient hors consentement, lesquels non, et comment un auditeur le vérifierait en pratique. Rapproche-le de l'affaire Fnac Darty traitée dans le dépôt.

**Angle 2 — Pseudonymisation et ré-identification.** Explique en détail la logique du nouvel article 25 bis sur la pseudonymisation : une donnée est-elle personnelle selon le destinataire ? Donne des exemples de jeux de données hachés ou tokenisés et de recoupements qui rendraient la ré-identification possible.

**Angle 3 — Architecture de notification d'incidents.** Compare le point d'entrée unique européen proposé par la Commission aux points d'entrée nationaux retenus par le Conseil, et discute l'impact sur l'automatisation de la notification NIS2 et RGPD dans un contexte multi-pays. Rappelle les articles 33 et 34 du RGPD.

**Angle 4 — Veille réglementaire automatisée.** Propose comment suivre automatiquement une procédure de codécision comme 2025/0360(COD) : sources officielles à surveiller, jalons attendus (position du Parlement, trilogue, adoption), et signaux faibles à scruter. Souligne la différence entre mandat du Conseil et loi.

**Angle 5 — Prospective et scénarios.** Imagine trois scénarios de résultat de la négociation avec le Parlement sur l'IA et l'intérêt légitime, en précisant ce que chacun changerait pour l'entraînement de modèles et pour les recours devant la CNIL ou la CJUE. Reste prudent sur ce qui n'est pas établi.

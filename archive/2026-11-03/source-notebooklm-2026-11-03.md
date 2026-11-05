# Source NotebookLM — France Titres, contrôles de la CNIL et sanction des organismes publics (3 novembre 2026)

## Contexte : un portail d'identité au cœur de la vie quotidienne

France Titres, nom d'usage de l'ancienne Agence nationale des titres sécurisés (ANTS, rebaptisée par le décret n° 2024-146 du 26 février 2024), gère les démarches liées aux titres sécurisés : cartes d'identité, passeports, permis, cartes grises. Son portail ants.gouv.fr concentre donc des comptes d'usagers contenant des données d'identité. Le 15 avril 2026, un incident de sécurité y a été détecté. Selon la presse, un vendeur sur des forums cybercriminels a proposé entre 12 et 18 millions de lignes ; la presse spécialisée a aussi évoqué environ 11,7 millions de comptes. Ces chiffres sont à manier avec prudence : une ligne de données n'est pas une personne, et le nombre de personnes réellement concernées n'a pas été établi dans les sources consultées. Les catégories évoquées sont des identifiants de connexion, civilité, noms, prénoms, date de naissance, adresse électronique et, pour une partie des dossiers, adresse postale, lieu de naissance et téléphone. Le ministère de l'Intérieur a indiqué que les pièces jointes n'étaient pas concernées.

## Ce qui s'est passé depuis

L'enquête pénale a été confiée au parquet de Paris, d'après la presse. Un mineur a été interpellé, ce qui ne préjuge en rien de sa culpabilité. Le 30 avril 2026, le Premier ministre Sébastien Lecornu s'est rendu dans les locaux de l'agence et a annoncé une « doctrine de protection » : fusion de la Dinum et de la DITP en une « autorité numérique de l'État », 200 millions d'euros via France 2030 pour la détection, les applications et la cryptographie post-quantique, des exercices d'« auto-attaque », et, pour 2027, 5 % des budgets numériques ministériels consacrés à la cybersécurité. La ministre déléguée Anne Le Hénanff a jugé cette somme insuffisante en soi et rappelé un minimum de 10 % du budget informatique.

Le développement nouveau date du 29 octobre 2026 : selon L'Informé, relayé le 30 octobre par FrenchBreaches, la présidente de la CNIL a ordonné des contrôles de France Titres, sur place ou à distance, à la suite de plusieurs plaintes. L'objectif serait de vérifier le respect de l'article 32 du RGPD. Point de méthode : à notre connaissance, cette information n'a pas pu être recoupée sur une publication de la CNIL elle-même ; elle repose sur un média secondaire qui dit avoir consulté un courrier de l'autorité. Il faut donc la traiter comme probable, non comme confirmée. Un avocat, Me Jérémy Roche, annonce par ailleurs préparer une action collective visant l'indemnisation de plusieurs centaines d'euros par victime ; aucune décision d'indemnisation n'existe.

## Les notions juridiques à maîtriser

Le RGPD organise une chaîne de responsabilités. L'article 32 impose au responsable de traitement et au sous-traitant de mettre en œuvre des mesures techniques et organisationnelles appropriées au risque : pseudonymisation et chiffrement le cas échéant, confidentialité, intégrité, disponibilité et résilience des systèmes, capacité à rétablir l'accès, et procédure de test régulier de l'efficacité des mesures. C'est une obligation de moyens adaptés, pas une garantie d'inviolabilité : subir une attaque ne prouve pas à lui seul un manquement. Ce qui est évalué, c'est la proportionnalité des protections au regard de l'état de l'art, du coût et de la nature des données. L'article 33 impose de notifier une violation à l'autorité de contrôle dans les 72 heures lorsqu'elle présente un risque, et l'article 34 d'informer les personnes lorsque le risque est élevé. L'article 58 du RGPD donne aux autorités des pouvoirs d'enquête, dont les audits et l'accès aux locaux et systèmes.

En France, la loi du 6 janvier 1978 distingue le contrôle de la sanction. Les agents de la CNIL contrôlent ; si un manquement est suspecté, le dossier peut conduire à une mise en demeure ou à une procédure devant la formation restreinte, qui peut prononcer un rappel à l'ordre, une injonction éventuellement sous astreinte (jusqu'à 100 000 € par jour), une limitation de traitement ou une amende administrative. Pour les obligations de sécurité, le plafond est de 10 M€ ou 2 % du chiffre d'affaires mondial, selon la CNIL ; il monte à 20 M€ ou 4 % pour les manquements aux principes fondamentaux. La décision est susceptible de recours devant le Conseil d'État.

## Le point délicat : peut-on mettre l'État à l'amende ?

L'article 83, paragraphe 7, du RGPD laisse chaque État membre décider si des amendes peuvent être infligées aux autorités et organismes publics. D'après une source secondaire, l'article 20, III de la loi de 1978 exclut l'amende administrative lorsque le traitement est « mis en œuvre par l'État » (ministères, administrations centrales), tandis que les autres personnes publiques, comme l'ANTS, seraient soumises aux plafonds de droit commun. Cette lecture doit être vérifiée sur le texte consolidé de Légifrance, et la qualification précise de France Titres (établissement public ou service de l'État) compte. Si l'amende était écartée, la CNIL conserverait ses autres outils, notamment l'injonction, la limitation du traitement et la publicité de sa décision, qui ont un effet réputationnel réel.

Sur le terrain pénal, l'article 226-17 du Code pénal punit le fait de traiter des données sans mettre en œuvre les mesures de sécurité prescrites, de cinq ans d'emprisonnement et 300 000 € d'amende. Pour une personne morale, l'amende est quintuplée, mais l'État, lui, est exclu de la responsabilité pénale des personnes morales par l'article 121-2 du Code pénal, d'après la même source secondaire : une plainte viserait alors des personnes physiques. Côté réparation, l'article 82 du RGPD ouvre un droit à indemnisation pour dommage matériel ou moral, et l'article 80 permet à des organismes de représenter les personnes.

## Enjeux

Le dossier met à l'épreuve trois idées. D'abord, la sécurité des données d'identité est un sujet d'infrastructure, pas seulement de conformité : un compte volé permet de l'hameçonnage ciblé et de l'usurpation. Ensuite, l'asymétrie de la sanction entre l'État et le secteur privé alimente un débat sur la crédibilité de la dissuasion ; l'annonce d'une affectation des amendes de la CNIL à un fonds de modernisation dans le prochain projet de loi de finances, rapportée par la presse, montre que le sujet est politique. Enfin, la durée entre incident (avril) et contrôle annoncé (fin octobre) rappelle que la procédure de la CNIL se compte en mois, voire en années : les sanctions récentes de ce dépôt, comme celle de 42 M€ contre Free Mobile et Free en janvier 2026, concernent des faits de 2024.

## Références

RGPD (règlement UE 2016/679), articles 32, 33, 34, 58, 80, 82, 83 ; loi n° 78-17 du 6 janvier 1978, notamment l'article 20 ; Code pénal, articles 121-2 et 226-17 ; décret n° 2024-146 du 26 février 2024 ; page CNIL sur les pouvoirs de la formation restreinte.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez l'un des cinq angles ci-dessous selon ce que vous cherchez à retirer de ce document.

**Angle 1 — Audit offensif : ce que la CNIL irait vérifier.** Concentre-toi sur ce qu'un contrôle de l'article 32 examine concrètement : segmentation, journalisation, gestion des comptes, protection contre l'énumération et l'extraction massive, tests d'intrusion. Traduis chaque point en point de contrôle qu'un pentester pourrait documenter, en précisant ce qui relève de la preuve technique.

**Angle 2 — Architecture d'un portail d'identité.** Discute de l'architecture typique d'un portail de comptes citoyens (authentification, API, exports, rate limiting) et des défauts qui rendent possible une extraction de millions de lignes. Distingue clairement ce qui est établi dans le dossier de ce qui est hypothèse.

**Angle 3 — Comparaison des régimes de sanction.** Compare ce dossier aux autres sanctions et fuites déjà traitées dans le dépôt (Free Mobile et Free, CTS, Orange, Fnac) : qui est sanctionnable, avec quel plafond, après combien de temps, et pourquoi l'État est un cas à part.

**Angle 4 — Veille réglementaire automatisée.** Explique comment automatiser la veille sur ce type de dossier : sources primaires à surveiller (CNIL, Légifrance, Conseil d'État), alertes sur les délibérations SAN-, distinction entre information de presse et publication officielle, et règles de fiabilité à appliquer avant de publier.

**Angle 5 — Prospective contentieuse.** Anticipe les scénarios : issue du contrôle, mise en demeure ou procédure de sanction, action de groupe et difficultés d'indemnisation du préjudice moral, recours devant le juge administratif. Indique les indicateurs qui permettraient de trancher entre ces scénarios dans les prochains mois.

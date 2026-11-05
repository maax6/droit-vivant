# Fuite de données à la CTS de Strasbourg : comprendre les obligations du RGPD après une violation

## Contexte : l'actualité du 28 octobre 2026

Le 28 octobre 2026, la Compagnie des transports strasbourgeois (CTS), qui exploite le réseau de bus et de tramway de l'agglomération de Strasbourg, a annoncé qu'environ 230 000 comptes clients avaient été concernés par une fuite de données. D'après les informations rapportées par la presse (notamment l'agence Anadolu, qui cite l'entreprise), les données ont été extraites par un usage illicite du site internet de la CTS. L'entreprise affirme avoir arrêté l'extraction dès sa détection et renforcé la sécurité du site. Les données exposées seraient des dates de naissance, des adresses postales et des identifiants clients. La CTS indique que ni les coordonnées bancaires ni les mots de passe ne sont concernés. Les clients ont été prévenus par courriel et invités à la vigilance, et la CNIL a été informée. Une plainte devant la justice strasbourgeoise était, selon un média local relayé, encore à déposer.

Un point de méthode s'impose : il s'agit d'une annonce de l'entreprise, relayée par la presse. Aucune décision de la CNIL ni aucune procédure n'est connue à ce jour, et rien ne permet de dire que la CTS a manqué à ses obligations. Ce module explique le cadre juridique applicable, pas une culpabilité.

## Qu'est-ce qu'une violation de données ?

Le règlement général sur la protection des données (RGPD, règlement (UE) 2016/679) définit à l'article 4, point 12, la violation de données à caractère personnel comme une violation de la sécurité entraînant, de manière accidentelle ou illicite, la destruction, la perte, l'altération, la divulgation non autorisée de données personnelles ou l'accès non autorisé à de telles données. La notion est large : elle couvre l'attaque informatique, mais aussi l'erreur humaine ou la perte d'un support. Elle se décline classiquement en trois atteintes : à la confidentialité, à l'intégrité et à la disponibilité.

L'extraction de données de comptes clients par un tiers est un cas typique d'atteinte à la confidentialité.

## Les trois obligations en cascade

Première obligation, en amont : la sécurité du traitement, article 32. Le responsable de traitement et le sous-traitant doivent mettre en œuvre des mesures techniques et organisationnelles appropriées au risque, en tenant compte de l'état de l'art et des coûts. Le texte cite notamment la pseudonymisation, le chiffrement, la capacité à garantir la confidentialité, ainsi que des tests réguliers de l'efficacité des mesures. L'obligation est de moyens renforcés, appréciée au cas par cas, et non une garantie d'invulnérabilité : une fuite ne prouve pas à elle seule un manquement.

Deuxième obligation, article 33 : la notification à l'autorité de contrôle, en France la CNIL. Elle doit intervenir dans les meilleurs délais et, si possible, 72 heures au plus tard après en avoir pris connaissance, sauf si la violation n'est pas susceptible d'engendrer un risque pour les droits et libertés des personnes. La notification peut être faite par étapes si toutes les informations ne sont pas disponibles. Le responsable de traitement doit en outre documenter toute violation, même non notifiée, dans un registre interne.

Troisième obligation, article 34 : la communication aux personnes concernées lorsque la violation est susceptible d'engendrer un risque élevé. Le message doit être rédigé en termes clairs et simples, décrire la nature de la violation, indiquer les conséquences probables, les mesures prises et les coordonnées du délégué à la protection des données ou d'un point de contact. Des exceptions existent, par exemple si les données étaient chiffrées de manière à être inintelligibles.

## Pourquoi des données « simples » restent dangereuses

On pourrait croire qu'une fuite sans mot de passe ni IBAN est sans gravité. C'est une erreur d'appréciation fréquente. Nom, date de naissance, adresse postale et identifiant client permettent de construire des messages d'hameçonnage très crédibles, par courriel, SMS ou courrier, en se faisant passer pour l'opérateur lui-même (« votre abonnement est suspendu, cliquez ici »). Ils permettent aussi des tentatives d'usurpation d'identité ou de prise de contrôle de comptes sur d'autres services, notamment par ingénierie sociale auprès de services clients. La qualification du risque, élevé ou non, est précisément l'enjeu de l'article 34 : plus les données permettent d'exploiter la victime, plus l'information individuelle est exigée.

## Le précédent Free : ce que sanctionne la CNIL

Pour comprendre la manière dont la CNIL raisonne, le précédent le plus récent est la sanction de 42 millions d'euros prononcée en janvier 2026 contre Free Mobile (27 M€) et Free (15 M€), délibérations SAN-2026-001 et SAN-2026-002 du 8 janvier 2026. À la suite d'une attaque d'octobre 2024 ayant donné accès aux données de millions de contrats d'abonnés, dont des IBAN, la formation restreinte a retenu des manquements à l'article 32 (authentification insuffisante sur le VPN, détection inefficace des comportements anormaux) et à l'article 34 (courriel d'information incomplet, ne permettant pas aux personnes de comprendre les conséquences ni de se protéger). Free Mobile a de plus été sanctionnée pour une conservation excessive de données d'anciens abonnés. Le cas CTS est sans commune mesure à ce stade, mais il illustre les mêmes questions : comment l'accès a-t-il été possible, a-t-il été détecté vite, et le message aux clients est-il utile ?

## Les amendes possibles

L'article 83 du RGPD prévoit deux paliers d'amendes administratives : jusqu'à 10 millions d'euros ou 2 % du chiffre d'affaires mondial pour les manquements aux obligations des articles 32 à 34, jusqu'à 20 millions ou 4 % pour les atteintes aux principes de base. La CNIL tient compte de la gravité, de la durée, du nombre de personnes, de la coopération et des mesures prises pour atténuer le dommage. Les personnes concernées disposent par ailleurs de recours individuels et, en France, de l'action de groupe en matière de données personnelles.

## Ce que peut faire une personne concernée

Les conseils usuels de la CNIL et de Cybermalveillance.gouv.fr sont de se méfier de tout message se référant à l'opérateur, de ne jamais cliquer sur un lien non vérifié, de changer ses mots de passe si une réutilisation est possible, d'activer l'authentification à deux facteurs, et de signaler les messages frauduleux (33700 pour les SMS, signal-spam.fr pour les courriels, plateforme Phishing Initiative). Elle peut exercer son droit d'accès auprès de l'opérateur et saisir la CNIL.

## Enjeux pour les professionnels

Pour une organisation qui exploite des comptes clients en ligne, trois leçons ressortent : prévoir un processus d'incident qui tient dans la fenêtre de 72 heures, avec qualification du risque documentée ; préparer des modèles de message aux personnes conformes à l'article 34 ; et traiter le portail client comme une surface d'attaque, avec limitation de débit, détection de l'énumération et du scraping, contrôle des accès aux objets et journalisation exploitable.

## Références

RGPD (règlement (UE) 2016/679), articles 4 point 12, 32, 33, 34 et 83 (EUR-Lex) ; CNIL, « Violations de données personnelles : les règles à suivre » ; CNIL, sanction Free Mobile et Free, SAN-2026-001 et SAN-2026-002 ; Anadolu Agency, 28 octobre 2026.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez l'un des cinq angles ci-dessous selon le focus souhaité pour l'épisode.

**Angle 1 — Audit offensif d'un portail client.** Concentre-toi sur les points de contrôle techniques qu'un test d'intrusion devrait vérifier sur un espace client web : contrôle d'accès aux objets (IDOR), limitation de débit, énumération d'identifiants, scraping automatisé, journalisation. Explique comment chacun se relie à l'obligation de sécurité de l'article 32.

**Angle 2 — Architecture et API.** Discute de l'architecture typique d'un site de transport avec comptes clients, des API exposées et des endroits où une extraction massive « via un usage illicite du site » est plausible, sans spéculer sur le cas CTS. Précise ce qu'on peut affirmer et ce qui reste inconnu.

**Angle 3 — Comparaison avec la sanction Free.** Compare le cas CTS à la sanction de 42 M€ contre Free Mobile et Free : manquements retenus aux articles 32 et 34, critères de la CNIL, différences de gravité. Insiste sur la qualité du message aux victimes.

**Angle 4 — Veille réglementaire automatisée.** Explique comment automatiser la veille sur les violations déclarées et les décisions de la CNIL (flux RSS, Légifrance, alertes), et comment structurer un registre de violations et un workflow de notification dans la fenêtre de 72 heures.

**Angle 5 — Prospective contentieuse.** Anticipe les suites possibles : contrôle ou procédure de la CNIL, plaintes, actions de groupe, responsabilité civile. Distingue clairement ce qui est établi, ce qui est annoncé et ce qui est hypothétique.

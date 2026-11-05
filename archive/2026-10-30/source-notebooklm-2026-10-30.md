# Fnac, la CNIL et les traceurs de l'application mobile : une sanction de 7 millions d'euros (SAN-2026-015)

## Contexte : pourquoi cette décision compte

Le 29 octobre 2026, la CNIL a rendu publique une sanction prononcée le 22 octobre 2026 par sa formation restreinte, la délibération SAN-2026-015. Elle vise deux sociétés du groupe Fnac Darty, Fnac Darty Participations et Services (FDPS) et Fnac Direct, coresponsables des traitements liés à l'application mobile Fnac. Le total atteint 7 millions d'euros : 6 millions pour FDPS et 1 million pour Fnac Direct. C'est une décision de première instance administrative, qui peut faire l'objet d'un recours devant le Conseil d'État. Aucune faute pénale n'est en cause : il s'agit d'un manquement à une règle de protection de la vie privée dans les communications électroniques.

## Les règles en jeu

Le texte central n'est pas le RGPD au sens strict mais l'article 82 de la loi Informatique et Libertés du 6 janvier 1978 (ancien article 32 II), qui transpose l'article 5(3) de la directive ePrivacy 2002/58/CE. Le principe : toute action visant à accéder, par voie de transmission électronique, à des informations déjà stockées dans l'équipement terminal d'un utilisateur, ou à inscrire des informations dans cet équipement, ne peut avoir lieu qu'à condition que la personne ait exprimé son consentement, après information claire et complète. Les exceptions sont étroites : opérations ayant pour seule finalité de permettre ou faciliter la communication électronique, ou strictement nécessaires à la fourniture d'un service expressément demandé. Le consentement dont il est question se mesure à l'aune de la définition du RGPD : libre, spécifique, éclairé et univoque.

Le vocabulaire « cookie » est trompeur. La notion juridique est celle de traceur, c'est-à-dire toute technique de lecture ou d'écriture sur le terminal. Dans une application mobile, il n'y a pas de cookie de navigateur, mais des identifiants publicitaires, des SDK et des appels d'API qui transportent un identifiant et des données d'activité. La CNIL applique le même raisonnement.

## Les faits relevés

Selon la CNIL, un contrôle effectué en mars 2024 faisait suite à une plainte de l'association NOYB. Les agents ont constaté que l'application mobile Fnac émettait des requêtes API vers un domaine tiers. Ces requêtes contenaient un identifiant de l'utilisateur ainsi que des informations sur son activité, par exemple les produits consultés. Ces données servaient à personnaliser les contenus et à entraîner l'algorithme de recommandation de produits. La formation restreinte relève que ces opérations ont eu lieu sans consentement préalable, y compris lorsque l'utilisateur avait cliqué sur « Continuer sans accepter », c'est-à-dire lorsqu'il avait exprimé un refus.

La CNIL écarte l'idée que ces opérations entrent dans les exceptions de l'article 82 : la personnalisation et l'entraînement d'un algorithme ne sont ni indispensables à la communication ni strictement nécessaires à un service expressément demandé. Elles exigeaient donc un consentement préalable.

## Sanction, calcul et injonction

La formation restreinte a prononcé une amende administrative de 6 millions d'euros contre FDPS et de 1 million d'euros contre Fnac Direct. Pour fixer ces montants, elle a pris en compte le chiffre d'affaires du groupe Fnac Darty, supérieur à 10 milliards d'euros en 2025, en retenant que la présomption d'influence déterminante de la société holding sur ses filiales n'était pas renversée. Les sociétés invoquaient un contexte réglementaire complexe, leur coopération et des difficultés financières ; ces arguments ont été écartés. La formation relève aussi que la CNIL avait déjà sanctionné des manquements similaires, ce qui pèse sur l'appréciation de la gravité.

Elle a assorti la sanction d'une injonction : démontrer, dans un délai d'un mois à compter de la notification, que le nouvel outil de recueil du consentement fonctionne lorsque le consentement est requis, sous astreinte de 10 000 euros par jour de retard. La délibération est publiée, sans identification nominative des sociétés au bout de deux ans. Parmi les textes visés figurent aussi le RGPD (notamment les articles 4(7), 31 et 83), le décret n° 2019-536 du 29 mai 2019 et la décision n° 2025-1154 QPC du Conseil constitutionnel, que la délibération vise sans que nous en détaillions ici la portée.

## Un enchaînement qui s'inscrit dans une série

La sanction de 42 millions d'euros contre Free Mobile et Free en janvier 2026 portait sur la sécurité des données et l'information des victimes d'une fuite. La présente décision relève d'un autre régime, celui des traceurs, mais elle confirme la même ligne : la CNIL sanctionne autant des défauts d'architecture que des défauts de formulation, et module l'amende sur la puissance économique du groupe. La fuite de la CTS à Strasbourg, traitée hier dans ce dépôt, relève encore d'un troisième terrain, la notification des violations de données.

## Enjeux pour les praticiens

Premier enjeu : le périmètre. Les applications mobiles, leurs SDK et leurs appels d'API sont soumis à la même exigence de consentement que les sites web. Deuxième enjeu : l'effectivité du refus. Une interface qui propose « Continuer sans accepter » mais continue d'émettre des appels porteurs d'identifiant est, d'après la formation restreinte, non conforme ; la conformité se vérifie donc dans le trafic réseau réel, pas dans le texte du bandeau. Troisième enjeu : la finalité. L'entraînement d'un algorithme de recommandation n'est pas une exception au consentement. Quatrième enjeu : la dimension groupe. Le chiffre d'affaires pris en compte est celui du groupe, ce qui change l'ordre de grandeur des amendes pour les filiales.

Pour le chercheur en sécurité, cette décision illustre aussi comment une plainte d'association peut déclencher un contrôle qui s'appuie sur de l'analyse de flux réseau : le contrôle de mars 2024 a porté sur des requêtes API observables. Il ne s'agit pas ici de qualifier un comportement individuel mais de comprendre ce que le régulateur vérifie et avec quels éléments de preuve.

## Limites et prudence

La décision reflète la position de la formation restreinte à ce stade. Les sociétés peuvent la contester devant le Conseil d'État. Les faits décrits sont ceux retenus par la CNIL, non ceux d'un juge. Ce module est pédagogique et ne constitue pas un conseil juridique personnalisé.

## Références

CNIL, communiqué « Cookies et application mobile : sanctions de 7 millions d'euros à l'encontre des sociétés FNAC DARTY PARTICIPATIONS ET SERVICES et FNAC DIRECT » ; Légifrance, délibération SAN-2026-015 du 22 octobre 2026 ; loi n° 78-17 du 6 janvier 1978, article 82 ; directive 2002/58/CE, article 5(3) ; règlement (UE) 2016/679.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez un seul angle et collez-le tel quel dans le champ de personnalisation.

**Angle 1 — Audit technique du trafic mobile.** Concentre-toi sur la manière dont on vérifierait techniquement la conformité d'une application mobile à l'article 82 : interception du trafic des requêtes API, repérage des identifiants envoyés à des domaines tiers, comparaison du comportement avant et après un refus de consentement. Explique quels éléments de preuve ont de la valeur pour un régulateur.

**Angle 2 — Architecture et API.** Décris l'architecture type d'une application de e-commerce avec moteur de recommandation : SDK, API, domaine tiers, identifiants. Identifie où se situent les opérations de lecture et d'écriture visées par l'article 82 et quels choix de conception permettent de les conditionner au consentement.

**Angle 3 — Comparaison avec les autres sanctions.** Compare cette sanction avec celle de 42 M€ contre Free Mobile et Free, et avec la logique de notification des violations vue avec la fuite de la CTS : régime juridique, manquement, calcul de l'amende, rôle du chiffre d'affaires du groupe. Fais ressortir ce que chaque régime exige de l'organisation.

**Angle 4 — Veille réglementaire automatisée.** Imagine un workflow de veille qui surveille les publications de la CNIL et de Légifrance, détecte les délibérations de sanction, extrait automatiquement montants, articles cités et injonctions, et alimente un tableau de suivi. Précise les champs à extraire et les pièges d'interprétation.

**Angle 5 — Prospective contentieuse.** Anticipe les suites : recours possible devant le Conseil d'État, arguments plausibles des sociétés, effet de la décision sur les autres éditeurs d'applications, rôle des plaintes d'associations. Distingue clairement ce qui est établi par la délibération de ce qui relève de l'hypothèse.

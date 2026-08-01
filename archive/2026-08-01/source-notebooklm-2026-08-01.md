# Moissonnage, IA générative et RGPD : ce que change le paquet CEPD du 7 juillet 2026

## Le point de départ : une confusion tenace

Il existe une idée reçue extraordinairement répandue, y compris chez des ingénieurs très compétents : ce qui est publiquement accessible en ligne serait, par nature, librement réutilisable. Une photo de profil consultable sans authentification, un avis laissé sur un site de commerce, une biographie sur une page institutionnelle, un message posté sur un forum ouvert — tout cela serait « public », donc disponible. Cette intuition est fausse en droit européen, et le Comité européen de la protection des données (CEPD) vient de le réaffirmer avec un niveau de détail inédit.

Le 7 juillet 2026, le CEPD, présidé par la Finlandaise Anu Talus, a adopté deux textes qui intéressent directement toute personne qui construit des pipelines de collecte automatisée : les lignes directrices 03/2026 sur le moissonnage dans le contexte de l'intelligence artificielle générative, et les lignes directrices 02/2026 sur l'anonymisation. Il a également finalisé, après consultation publique, ses lignes directrices sur le traitement de données au moyen des technologies de chaîne de blocs. La CNIL a relayé l'ensemble le 9 juillet 2026. Les deux premiers textes sont en version 1.0 et soumis à consultation publique jusqu'au 30 octobre 2026 : ils ne sont donc pas figés, ce qui constitue en soi une information stratégique pour les acteurs techniques.

## Ce qu'est le moissonnage, et pourquoi le droit s'y intéresse

Le moissonnage — *web scraping* — désigne l'extraction automatisée et à grande échelle de données depuis des sites web. Sa caractéristique juridiquement décisive, soulignée par le CEPD, est qu'il opère le plus souvent sans que les personnes concernées en aient la moindre conscience. C'est précisément cette asymétrie qui fonde l'intérêt du régulateur : la personne dont les données sont aspirées n'a ni notification, ni interlocuteur, ni généralement moyen de savoir que ses données alimentent l'entraînement d'un modèle.

Le raisonnement juridique est mécanique. Le RGPD s'applique à tout traitement de données à caractère personnel ; or le moissonnage emporte typiquement une collecte, un stockage, une organisation et une extraction — soit quatre opérations expressément visées par la définition du traitement. La publicité de la donnée n'est pas une base légale : ce n'est ni un consentement, ni un contrat, ni une obligation légale. Elle ne change rien à la qualification.

## Les principes que le CEPD met en avant

Trois principes reçoivent une attention particulière dans les lignes directrices 03/2026.

Le premier est la **limitation des finalités**, à l'article 5 § 1 b du RGPD. On ne collecte pas « pour voir » : la finalité doit être déterminée, explicite et légitime avant la collecte, et l'usage ultérieur des données doit rester compatible avec elle. Un corpus moissonné pour une finalité de recherche ne bascule pas librement vers un entraînement commercial.

Le deuxième est la **transparence**, aux articles 13 et 14. Le CEPD admet ici une nuance importante : selon la conception précise du traitement, le responsable peut ne pas avoir à informer individuellement chaque personne si cela s'avère impossible ou exige des efforts disproportionnés — c'est la logique de l'article 14 § 5 b. Mais cette dispense d'information individuelle n'est pas une dispense de transparence : elle appelle des mesures alternatives, typiquement une information publique sur les sources, les finalités et les modalités d'opposition.

Le troisième est l'**exactitude**, à l'article 5 § 1 d, et c'est peut-être le passage le plus opérationnel du texte. Le CEPD recommande explicitement de n'extraire que depuis des sources fiables, d'enregistrer l'horodatage de la collecte et de valider les données avant leur utilisation dans un entraînement. Traduit en termes d'ingénierie : il faut une provenance traçable, des métadonnées temporelles et une étape de validation dans le pipeline. Ce sont des exigences d'architecture, pas de rédaction juridique. Le CEPD assortit cela de recommandations sur la **minimisation** — filtrer ce dont on n'a pas besoin, plutôt que tout aspirer et trier après coup.

## L'intérêt légitime : la base légale de fait, et ses conditions

Dans la pratique, la seule base légale mobilisable pour du moissonnage à grande échelle est l'intérêt légitime de l'article 6 § 1 f. Le CEPD, prolongeant son avis 28/2024 sur les modèles d'IA, fournit des précisions et des exemples spécifiques à ce contexte. Le test reste en trois temps : existe-t-il un intérêt légitime réel et actuel ; le traitement est-il nécessaire pour l'atteindre, au sens où un moyen moins intrusif ne suffirait pas ; et la mise en balance avec les droits et libertés des personnes concernées tourne-t-elle en faveur du responsable, compte tenu notamment de leurs attentes raisonnables ?

La conséquence pratique est que cette mise en balance doit être **écrite, datée et propre à chaque traitement**. Un document générique valant pour tous les crawls d'une organisation ne satisfait pas l'exigence. C'est ce point qui, dans les affaires contentieuses passées, a le plus souvent départagé les acteurs.

## Les catégories particulières : le point dur

Le RGPD interdit par principe, à l'article 9 § 1, le traitement des données révélant l'origine raciale ou ethnique, les opinions politiques, les convictions religieuses ou philosophiques, l'appartenance syndicale, ainsi que les données de santé, celles concernant la vie ou l'orientation sexuelle, et les données génétiques et biométriques. Or un moissonnage massif du web en collecte inévitablement.

Le CEPD rappelle qu'un tel traitement suppose cumulativement une base légale au titre de l'article 6 et une exception au titre de l'article 9 § 2. Il suggère que le raisonnement de l'arrêt de la Cour de justice dans l'affaire GC e.a. contre CNIL (C-136/17, grande chambre, 24 septembre 2019) — rendu à propos du déréférencement par les moteurs de recherche — peut être pertinent pour la collecte **accessoire ou résiduelle** de telles données, à condition que le responsable agisse dans le cadre de ses « responsabilités, pouvoirs et capacités » et mette en œuvre des mesures techniques et organisationnelles appropriées pour empêcher leur collecte et leur diffusion. Le comité assortit immédiatement cette ouverture d'un avertissement sans ambiguïté : il n'existe **aucune exemption générale** aux exigences de l'article 9, et chaque situation doit être appréciée individuellement.

## L'anonymisation, ou la porte de sortie qui n'en est pas toujours une

Le second texte du 7 juillet complète le premier. Beaucoup d'organisations considèrent l'anonymisation comme la voie d'évitement du RGPD : données anonymes, règlement inapplicable. C'est exact — encore faut-il que l'anonymisation soit réelle.

Les lignes directrices 02/2026 clarifient la notion, en tenant compte notamment de l'arrêt CJUE du 4 septembre 2025, CEPD contre CRU (C-413/23 P). Le raisonnement retenu est relatif : une même donnée peut être anonyme pour une entité et personnelle pour une autre, selon les moyens raisonnablement susceptibles d'être mis en œuvre. Une personne est « identifiée ou identifiable » si elle peut être distinguée des autres dans un contexte donné, d'une manière permettant de la traiter différemment.

Le CEPD propose un cadre pratique articulé autour de trois critères : pas d'individualisation d'un enregistrement, pas de corrélation entre enregistrements, pas d'inférence. Si les trois sont satisfaits, les données peuvent être tenues pour anonymes en toute sécurité. Sinon, une analyse plus poussée s'impose. Deux modes d'application coexistent : une « approche contextuelle », qui évalue les différences de capacités entre les entités susceptibles de réidentifier et reflète toutes les nuances de la norme juridique ; et une « approche simplifiée », qui ignore ces différences, va potentiellement au-delà de ce qu'exige le droit, mais offre davantage de confiance et de simplicité opérationnelle.

## Le rappel des sanctions : Clearview AI

L'enjeu n'est pas théorique. En septembre 2024, l'autorité néerlandaise de protection des données, l'Autoriteit Persoonsgegevens, a infligé à la société américaine Clearview AI une amende de 30,5 millions d'euros, assortie d'astreintes pouvant dépasser cinq millions d'euros. Le grief : avoir constitué, par moissonnage du web, une base de données de milliards de photographies de visages, incluant des personnes résidant aux Pays-Bas, traitée sans base légale au sens des articles 5 § 1 et 6 § 1, et portant sur des données biométriques au sens de l'article 9 § 1. Clearview AI avait déjà été sanctionnée à hauteur de vingt millions d'euros par l'autorité italienne et par l'autorité grecque en 2022, et l'autorité française lui avait imposé une astreinte en 2023 ; l'autorité autrichienne a également rendu une décision constatant des manquements aux articles 5, 6, 9 et 27.

## Ce qu'il faut retenir

Le paquet du 7 juillet 2026 ne crée pas de nouvelle interdiction : il explicite comment des règles existantes s'appliquent à une pratique technique devenue industrielle. Son effet réel est de déplacer l'examen de la conformité du résultat vers le **processus** : la provenance des données, l'horodatage, le filtrage en amont, l'exclusion documentée des catégories particulières, et une mise en balance écrite antérieure à la collecte. La consultation publique ouverte jusqu'au 30 octobre 2026 est, pour les acteurs techniques, la fenêtre pendant laquelle il est encore possible de faire valoir ce qui est réellement implémentable côté crawler, robots.txt, journalisation et filtrage sémantique.

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Voici cinq angles au choix, adaptés à un profil de chercheur en cybersécurité et consultant en automatisation offensive. Chacun est prêt à être collé tel quel dans le champ de personnalisation de l'Audio Overview.

**Angle 1 — Le pipeline de scraping comme objet auditable.** Concentre-toi exclusivement sur ce qu'un auditeur devrait pouvoir vérifier dans un pipeline de moissonnage : provenance des sources, horodatage de collecte, étape de validation avant entraînement, mécanisme de filtrage des catégories particulières, journalisation. Formule des points de contrôle concrets, comme une check-list d'audit technique, et indique pour chacun quel article du RGPD ou quel passage des lignes directrices 03/2026 le fonde.

**Angle 2 — Architecture et implémentation : ce que le texte exige réellement du crawler.** Traduis les principes juridiques en contraintes d'architecture logicielle. Discute robots.txt et son statut juridique incertain, la gestion des rate limits, la déduplication, la conservation des en-têtes HTTP comme preuve de provenance, la séparation entre corpus brut et corpus validé, et les stratégies de filtrage en amont plutôt qu'en aval. Sois technique et concret, en supposant un auditeur familier des systèmes distribués.

**Angle 3 — Comparaison des régimes de sanction déjà couverts dans ce dépôt.** Mets en perspective les sanctions Clearview AI (30,5 M€ aux Pays-Bas, 20 M€ en Italie et en Grèce, astreinte en France) avec les autres régimes déjà documentés dans les modules précédents de Droit Vivant : l'amende DMA de 890 M€ infligée à Google le 23 juillet 2026, les plafonds de l'AI Act (15 M€ ou 3 % du chiffre d'affaires pour l'article 50, jusqu'à 35 M€ ou 7 % pour les manquements les plus graves), et les plafonds RGPD de 20 M€ ou 4 %. Explique ce que la comparaison révèle des priorités du régulateur européen.

**Angle 4 — Veille réglementaire automatisée : exploiter la fenêtre de consultation.** Traite le sujet sous l'angle de l'automatisation de la veille. Explique comment surveiller programmatiquement les publications du CEPD et de la CNIL, comment structurer une contribution à la consultation publique ouverte jusqu'au 30 octobre 2026, et quels signaux techniques (versions successives des lignes directrices, rapports de consultation, avis article 64) permettent d'anticiper la position finale du comité avant sa publication.

**Angle 5 — Prospective contentieuse : où se situeront les litiges.** Projette-toi sur les deux prochaines années et identifie les points de friction les plus probables : la qualification de la collecte « accessoire ou résiduelle » de catégories particulières au sens de l'arrêt C-136/17, la portée réelle de la dispense d'information de l'article 14 § 5 b pour les corpus massifs, la ligne de partage entre approche contextuelle et approche simplifiée de l'anonymisation après l'arrêt C-413/23 P, et l'articulation entre ces lignes directrices et les obligations de documentation des données d'entraînement prévues par l'AI Act. Formule chaque point comme une question qu'un tribunal devra trancher.

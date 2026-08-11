# Le texte qui porte sa propre signature — marquage des contenus générés par IA, article 50 de l'AI Act (12 août 2026)

## Une obligation qui ne ressemble pas à ce qu'on croit

Depuis le 2 août 2026, une règle européenne s'applique aux systèmes d'intelligence artificielle générative : leurs sorties doivent être marquées. Le mot induit en erreur. On imagine une mention visible, un bandeau « contenu généré par IA », une case à cocher. Ce n'est pas cela.

L'**article 50, paragraphe 2, du règlement (UE) 2024/1689** — l'AI Act — dispose que les fournisseurs de systèmes d'IA, y compris à usage général, générant du son, de l'image, de la vidéo ou du **texte** de synthèse, veillent à ce que les sorties soient « marquées dans un format **lisible par machine** et détectables comme ayant été générées ou manipulées par une IA ». Le destinataire du signal n'est donc pas l'être humain qui lit : c'est la machine qui analyse. Le texte impose ensuite des solutions « efficaces, interopérables, solides et fiables **dans la mesure où cela est techniquement possible** », compte tenu des limites propres à chaque type de contenu, du coût de mise en œuvre et de « l'état de l'art généralement reconnu ».

Cette phrase définit la nature exacte de l'obligation : elle n'est pas absolue, elle est bornée par la faisabilité technique et par l'état de l'art. C'est une obligation de moyens renforcés, pas une obligation de résultat probatoire. Le législateur savait que le marquage de texte est un problème scientifique ouvert, bien plus fragile que celui de l'image, et il a écrit la règle en conséquence. L'article prévoit d'ailleurs ses propres exceptions : fonction d'assistance à l'édition standard, absence de modification substantielle des données d'entrée ou de leur sémantique, ou autorisation légale à des fins de détection et de poursuite d'infractions pénales.

## Le code de bonnes pratiques, ou la conformité par mutualisation

Le paragraphe 7 du même article confie au **Bureau de l'IA** le soin de faciliter l'élaboration de codes de bonnes pratiques au niveau de l'Union. C'est chose faite : le **10 juin 2026**, la Commission publie le **Code of Practice on Transparency of AI-generated Content**, rédigé par des experts indépendants dans un processus multipartite entamé en septembre 2025. Il comporte deux sections calquées sur l'article 50 — la **section 1** pour les **fournisseurs** (marquage et détection), la **section 2** pour les **déployeurs** (étiquetage des deepfakes et de certains textes).

La Commission et le **comité IA** l'ont conjointement jugé adéquat. La conséquence pratique est souvent mal comprise : le code reste **volontaire**, mais l'obligation de l'article 50 demeure **légale**. Signer offre une voie de conformité présumée reconnue simultanément dans les vingt-sept États membres ; ne pas signer reste licite, mais impose de démontrer l'adéquation de sa propre approche devant chaque autorité nationale de surveillance du marché, une par une. Le code achète de la prévisibilité plus qu'il n'impose de contrainte.

Fin juillet 2026, **environ 190 organisations** l'avaient signé — 82 pour la section 1, 152 pour la section 2, dont environ la moitié de petites entreprises récentes. Section 1 : **Anthropic**, **Google**, **Meta**, **Microsoft**, **Mistral**, **OpenAI**, **Cohere**, **Aleph Alpha**, **Black Forest Labs**, **Synthesia**. Section 2 : **Bulgari**, **Getty Images**, **Iberdrola**, **Lenovo**, **Lufthansa**, mais aussi la Banque nationale de Roumanie et la Cour des comptes européenne.

## Ce qu'Anthropic a annoncé, et comment

Les 10 et 11 août 2026, la presse spécialisée relaie la mise en œuvre annoncée par **Anthropic**, qui a signé la section 1 en tant que fournisseur de modèles *et* de systèmes d'IA générative. Sa documentation publique décrit deux techniques complémentaires, qu'il vaut la peine de distinguer : elles n'ont ni la même robustesse ni les mêmes modes d'échec.

Pour le **texte**, un filigrane imperceptible est tissé directement dans la sortie au moment de la génération, sans modifier le sens, la qualité ni la lisibilité de la réponse. Le point décisif est qu'il est appliqué **au niveau du modèle**, et non de l'interface : il est donc présent quel que soit le produit par lequel le texte sort — API, application, Claude Code, Claude Cowork, Claude Tag — et jusque dans les accès via **AWS**, **Google Cloud** ou **Microsoft Foundry**. Parce que la marque fait partie du texte lui-même, elle **voyage avec le copier-coller** et peut survivre à certaines modifications.

Pour les **fichiers** pris en charge — `.svg`, `.png`, `.jpg` —, la technique est tout autre : des métadonnées de provenance **signées cryptographiquement**, conformes au standard ouvert **C2PA** (*Coalition for Content Provenance and Authenticity*). Une signature valide indique que le fichier a été traité par le modèle et permet de détecter si les données de provenance ont été altérées.

Deux paramètres de périmètre comptent. Le calendrier : le marquage vaut pour les modèles lancés **à compter du 2 août 2026**, les modèles antérieurs relevant du régime transitoire, avec un travail d'ajout en cours. La géographie, surtout : le marquage s'applique **partout où Claude est proposé, dans le monde entier**, et non aux seuls utilisateurs de l'Union.

## L'effet Bruxelles, par l'ingénierie plutôt que par le droit

Le règlement s'applique au marché de l'Union ; il n'a pas d'effet extraterritorial sur un échange entre un utilisateur brésilien et un serveur américain. Si un utilisateur japonais reçoit malgré tout du texte marqué, ce n'est pas parce que le droit européen l'a voulu, mais parce que **le marquage a été implanté au niveau du modèle**, où il devient indissociable de la sortie. Segmenter par région aurait supposé maintenir deux comportements de génération distincts : coût d'ingénierie, risque de divergence, complexité de test. C'est l'effet Bruxelles dans sa forme la plus pure — non pas l'extension juridique d'une norme, mais son extension par l'économie de l'architecture.

## Les limites, écrites par l'émetteur lui-même

La partie la plus utile de la documentation d'Anthropic est celle qui énonce ce que la marque **ne prouve pas**. Deux séries de limites, symétriques.

D'abord, une marque détectée n'établit pas la paternité : elle signale que le contenu **a pu être traité** par le modèle. Or on utilise couramment ces outils pour relire, traduire, résumer ou convertir — la sortie porte alors la marque alors même que les idées ou les données proviennent d'ailleurs. Le contenu peut aussi avoir été modifié, tronqué ou fusionné après traitement.

Ensuite, l'absence de marque n'établit pas l'origine humaine. Le texte peut venir d'un modèle antérieur au dispositif ; avoir été lourdement édité, paraphrasé, traduit ou fondu dans un ensemble plus large ; le passage peut être trop court pour porter un signal fiable ; les métadonnées d'un fichier peuvent avoir été effacées par conversion de format, ré-enregistrement ou capture d'écran.

Ni faux positifs ni faux négatifs ne sont donc des accidents ici : ce sont des propriétés structurelles du dispositif, assumées et documentées.

## Où porte réellement la contrainte

Le manquement à l'article 50 relève de l'**article 99, paragraphe 4, point g)** : amendes administratives jusqu'à **15 millions d'euros** ou **3 % du chiffre d'affaires annuel mondial total** de l'exercice précédent, le montant le plus élevé étant retenu. C'est le palier intermédiaire, le même que pour les obligations des fournisseurs et déployeurs de systèmes à haut risque — pas celui des pratiques interdites de l'article 5, qui atteint 35 millions d'euros ou 7 %.

Un point de calendrier, souvent mal suivi : le **règlement (UE) 2026/1744** dit « Digital Omnibus on AI » a **raccourci de six à trois mois** le délai de grâce applicable au marquage lisible par machine, fixant la butée au **2 décembre 2026** pour les systèmes mis sur le marché avant le 2 août 2026. Ce même texte a par ailleurs reporté à 2027 et 2028 le gros des obligations « haut risque » — mais il a resserré celle-ci. La transparence n'a pas été assouplie ; elle a été accélérée.

Enfin, l'obligation qui touche véritablement le public n'est pas celle du fournisseur. L'**article 50, paragraphe 4**, fait peser sur le **déployeur** la divulgation des deepfakes — contenu image, audio ou vidéo ressemblant à des personnes, objets, lieux ou événements existants et qui apparaîtrait faussement authentique — ainsi que celle des textes « publiés dans le but d'informer le public sur des questions d'intérêt public ». Avec une exemption majeure : cette dernière ne s'applique pas lorsque le contenu a fait l'objet d'une **revue humaine ou d'un contrôle éditorial** et qu'une personne assume la **responsabilité éditoriale** de la publication. La rédaction protège la presse ; elle expose, en creux, la publication automatisée sans relecture.

## Pour un praticien de la sécurité et de l'automatisation

D'abord une question de surface d'exposition : tout pipeline qui fait transiter du texte par un modèle marqué produit désormais un artefact qui persiste au copier-coller. La situation rappelle celle des métadonnées EXIF il y a quinze ans, quand une photographie publiée révélait un modèle d'appareil et des coordonnées GPS que personne n'avait pensé à retirer.

Ensuite une question de preuve : un marché d'outils de détection tiers va se former, et ses faux positifs auront des conséquences réelles — plagiat académique, contentieux du travail, décisions de modération. Le décalage est frappant entre l'usage social qui sera fait de ce signal et ce que son émetteur en dit : « pas concluant ».

Enfin une question de veille. La bonne question n'est pas « ce texte est-il marqué ? », mais « quel poids probatoire une autorité, une plateforme ou un juge acceptera-t-il d'accorder à un signal que le fournisseur déclare lui-même non concluant ? ». Aucune juridiction ne l'a encore tranchée.

*Contenu pédagogique ; ne constitue pas un conseil juridique personnalisé.*

## Angles de lecture pour NotebookLM (à coller dans « Personnaliser » de l'Audio Overview)

Choisissez l'un des cinq angles ci-dessous et collez-le tel quel dans le champ de personnalisation de l'Audio Overview, selon l'usage que vous voulez faire de ce module.

**Angle 1 — Surface d'exposition et hygiène des pipelines.** Traite ce document comme une note de sécurité opérationnelle. Explique où un filigrane textuel appliqué au niveau du modèle apparaît dans une chaîne de traitement réelle : génération, copier-coller, export, agrégation dans un livrable. Compare avec la fuite historique par métadonnées EXIF pour montrer ce qui se répète. Détaille ce qu'une revue de code ou une revue de processus devrait vérifier avant publication d'un contenu produit par un pipeline automatisé, sans jamais présenter cela comme une méthode d'effacement de marque.

**Angle 2 — Robustesse, faux positifs et théorie de la détection.** Concentre-toi sur la mécanique du signal. Explique pourquoi un filigrane statistique dans du texte est intrinsèquement moins robuste qu'une signature cryptographique attachée à un fichier, et pourquoi la longueur du passage conditionne la fiabilité de la détection. Développe les deux séries de limites documentées — marque présente sans paternité, marque absente sans origine humaine — et ce qu'elles impliquent pour toute décision automatisée fondée sur un détecteur.

**Angle 3 — Architecture, API et périmètre produit.** Prends l'angle du concepteur de systèmes. Analyse ce que signifie « marquage au niveau du modèle » plutôt qu'au niveau de l'interface, et pourquoi cela emporte l'application du dispositif à toutes les surfaces — API, applications, agents de code — ainsi qu'aux accès par plateformes cloud tierces. Discute des conséquences pour une entreprise qui intègre le modèle dans son propre produit, notamment la répartition des obligations entre fournisseur et déployeur au titre des paragraphes 2 et 4 de l'article 50.

**Angle 4 — Veille réglementaire et comparaison avec les modules précédents.** Utilise ce cas pour illustrer la veille des textes mouvants. Souligne que le calendrier de l'article 50 a été modifié après coup par le Digital Omnibus, dans le sens de l'accélération pour le marquage alors que le gros du régime « haut risque » était reporté — un point déjà documenté dans ce dépôt. Compare la mécanique du code de bonnes pratiques volontaire, qui mutualise la conformité auprès de vingt-sept autorités, avec d'autres dispositifs déjà traités ici, notamment les lignes directrices du CEPD sur le moissonnage et la répartition des compétences entre régulateurs.

**Angle 5 — Prospective contentieuse.** Projette la suite. Interroge la valeur probatoire que juges, universités, employeurs et plateformes accorderont à un signal dont l'émetteur écrit qu'il n'est pas concluant. Examine les terrains de contentieux prévisibles : accusation de plagiat fondée sur un détecteur, litige du travail, contestation d'une décision de modération, différend contractuel sur l'origine d'un livrable. Termine sur la question de l'interopérabilité : que se passe-t-il quand plusieurs fournisseurs déploient des marques incompatibles, et ce que l'exigence d'« interopérabilité » de l'article 50 § 2 pourra imposer en pratique.

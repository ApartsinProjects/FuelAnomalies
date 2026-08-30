# Cover letter

Dear Editor-in-Chief,

We submit our manuscript, **"Driver or Vehicle? Multi-Source Signature Attribution of Excess Fuel
Consumption Under Missing Joint Cause Labels,"** for consideration in *Engineering Applications of
Artificial Intelligence*.

**Problem and contribution.** When a vehicle burns more fuel than expected, a fleet operator must
decide between two very different remedies: coach the driver or service the vehicle. The two causes
share one symptom, and a fuel-per-distance figure cannot separate them. The obstacle to solving this
with machine learning is that no public dataset jointly labels the competing causes. We formulate the
task as **multi-source signature attribution under missing joint cause labels** (Algorithm 1): a
cause-specific signature is learned in each source domain that carries that cause's ground truth, the
signatures are frozen, and attribution is performed on the target fleet with an abstention option. We
instantiate it for excess fuel with a kinematic (driver) signature and a combustion (fault) signature,
and show that when fuel magnitude is made uninformative, frozen source-derived signatures attribute the
cause at 88.6% (a trained upper bound of 95.9%) where fuel magnitude alone is at chance.

**Fit to EAAI.** The work is an AI method solving a real engineering problem and is validated entirely
on public data, matching the journal's emphasis on intelligent transportation, intelligent fault
diagnosis, and reproducibility. We build on and extend the closest prior work in this journal, Barbado
and Corcho (EAAI, 2022), which detects fuel-consumption anomalies with explainable feature relevance;
our increment is to attribute the driver-versus-vehicle **cause**, with each signature validated in an
independent source domain, rather than to rank features of a single anomaly. Evidence spans a
197-vehicle public fleet (Vehicle Energy Dataset), a controlled engine-fault bench (EngineFaultDB), and
two independent driver-behaviour datasets, with a semi-synthetic bridge for the competing-cause
evaluation that no single real dataset supports. Every reported number traces to a released script.

**Declarations.** This manuscript is original, is not under consideration elsewhere, and has not been
published previously. All datasets are public and are cited; no data are redistributed. The authors
declare no competing interests. All authors have approved the submission.

We believe the paper will interest EAAI readers working on intelligent vehicles, fleet analytics, and
diagnostics, and we thank you for considering it.

Sincerely,

Alexander Apartsin, School of Computer Science, Faculty of Sciences, Holon Institute of Technology
(HIT), Holon, Israel (corresponding author)

Yehudit Aperstein, Intelligent Systems, Afeka Academic College of Engineering, Tel-Aviv, Israel

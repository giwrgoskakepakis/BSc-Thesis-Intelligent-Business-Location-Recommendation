The good news is that most of the weaknesses I identified are fixable without changing the core contribution of the paper. In fact, addressing them would significantly strengthen the paper and improve its chances for a stronger journal acceptance.

1. Replace or Strengthen the Proxy Ground Truth
This is the most important issue.

Currently the paper evaluates whether the LLM reproduces the ensemble recommendations rather than whether the recommendations are actually good.  

Option A (Best)
Use business success indicators:

Years in operation
Business survival rate
Number of reviews
Average rating
Rating × number of reviews
Business density growth
For example:

Success Score =
0.4 × SurvivalYears +
0.3 × Rating +
0.3 × ReviewCount

Then train and evaluate against that.

Option B (Realistic)
If success data are unavailable:

Rename throughout the paper:

Instead of

“ground truth”

use

“ensemble-generated target”

or

“algorithmic recommendation target”

This immediately removes a major reviewer criticism.

2. Add Human Expert Validation
A reviewer will ask:

“Do these recommendations make sense?”

Recruit:

3–5 business consultants
local chamber of commerce experts
entrepreneurs
Provide them:

30 business queries
top-3 recommendations
Ask them to score:

1–5 scale

for:

plausibility
usefulness
realism
Then report:

Expert agreement = 4.2/5

This single addition would dramatically strengthen the paper.

3. Add Statistical Significance Testing
Current table:

Model

Match@3

Fine-tuned

0.780

RAG

0.830

A reviewer will ask:

Is 0.830 really better?

Run:

bootstrap confidence intervals
paired t-test
Wilcoxon signed-rank
Report:

Match@3 = 0.830 ± 0.03

This takes only a few lines of code.

4. Explain Why Precision@3 = Recall@3
A reviewer will immediately notice this.

In your setup:

Ground truth = Top-3
Recommendation = Top-3
Therefore

Precision@3 = Recall@3

because denominator sizes are identical.

Add one sentence explaining this.

Otherwise reviewers may suspect an error.

5. Sensitivity Analysis of Ensemble Weights
Currently weights are:

0.311
0.358
0.331  
Reviewer question:

What happens if weights change?

Run:

equal weights
random weights
supervised-heavy weights
If rankings remain stable:

This becomes a strength.

6. Reduce Claims About Generalization
Current wording is too strong.  

Replace:

“generalization to unseen queries”

with

“generalization within the synthetic query distribution”

Similarly:

Replace:

“region agnostic”

with

“potentially transferable to regions with comparable data availability”

Reviewers like careful wording.

7. Demonstrate Hallucination Reduction
Currently:

RAG has lower hallucination risk.  

But there is no measurement.

Add:

50 manually reviewed queries.

Count:

nonexistent neighborhood references
incorrect feature claims
contradictory statements
Then report:

Hallucination rate:

Fine-tuned: 8%
RAG: 2%
Even a small study would help.

8. Expand the Evaluation Set
Current:

159 synthetic queries.  

Add:

50–100 real queries.

Examples:

“I want a quiet area near the university.”
“Open a café near the port.”
“Family-oriented neighborhood.”
This makes the evaluation more realistic.

9. Improve the Fine-Tuning Dataset
Current:

918 training examples.  

For a 7B model this is very small.

Generate:

10–20 prompt variants per NACE class
instead of 3.

Then you get:

3000–6000 examples

which reviewers will find more convincing.

10. Strengthen the Future Work Section
The most promising addition is already in your paper:

the collaborative filtering formulation.  

I would actually move part of that section earlier and present it as:

“A second evaluation framework based on held-out business-location interactions.”

This directly addresses the biggest criticism (proxy targets).

What I Would Do Before Submission
If I were revising this paper, I would prioritize:

Essential
Rename “ground truth” → “proxy target”.
Add significance testing.
Explain Precision=Recall.
Add expert evaluation.
Tone down generalization claims.
Strongly Recommended
Add real-user queries.
Sensitivity analysis of ensemble weights.
Hallucination evaluation.
Future Journal Version
Business survival/success labels.
Collaborative filtering + LLM hybrid evaluation.
If you implement just the Essential changes, I believe the paper would move from roughly a 7.5–8/10 paper to an 8.5+/10 paper, because most reviewers will focus on evaluation rigor rather than the underlying idea, which is already quite interesting and novel.
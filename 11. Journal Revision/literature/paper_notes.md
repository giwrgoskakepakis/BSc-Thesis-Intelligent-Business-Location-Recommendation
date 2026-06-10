This is a file where I keep track of the papers I read, relevant important notes for each paper and more.

# Papers Read

I have read the following papers, and I include useful notes for each:

## 1. Collaborative Filtering for Implicit Feedback Datasets

- Introduces the concept of **implicit feedback** RS
- Utilization of **preference/confidence**
- Uses a **MF model**
- Evaluation with **rank** metric

---

## 2. Bayesian Personalized Ranking from Implicit Feedback

- Follows the axes of implicit feedback
- Introduces the concept of **pair-wise framing** for optimization
- Uses 2 simple RS models (MF/kNN) by applying BPR

---

## 3. Neural Collaborative Filtering

- Follows the axes of imlicit feedback
- Introduces the concept of **NCF**
- Proposes 3 NCF models: **GMF/MLP/NeuMF**
- Compares with baselines such as MF-BPR

---

## 4. Performance of Recommender Algorithms on Top-N Recommendation Tasks

- Suggests that **accuracy metrics (Precision/Recall) may be more useful than error metrics (MSE)** for top-N recommendation tasks
- Introduces 2 models that operate on accuracy metrics (NNCosNgbr/PureSVD)
- Compares with baselines such as MovieAvg/TopPop/...

---

## 5. Advances and Challenges in Conversational Recommendation Systems

- Introduces the concept of **Conversational Recommendation Systems (CRS)** (based on **multi-turn** dialoge)
- Creates a general framework for CRS
- Addresses the 5 main challenges of CRS



# General Notes

Some useful notes/concepts derived from studying all the papers above: 

## 1. Different Axes

From what I understand, there are multiple 'different axes', meaning different choices that each approach 
uses, which are not related. In particular, I have extracted the following axes: 

- Feedback type: explicit, implicit
- Model architecture: MF, SVD, GMF, MLP, NeuMF, ...
- Optimization Framing: Point-wise, Pair-wise

We can use these axes to frame the approaches used in the papers and compare them: 

- 1. Collaborative Filtering for Implicit Feedback Datasets --> (implicit, MF, point-wise)
- 2. Bayesian Personalized Ranking from Implicit Feedback --> (implicit, MF/kNN, pair-wise)
- 3. Neural Collaborative Filtering --> (implicit, GMF/MLP/NeuMF, point-wise), compared with (implicit, MF, pair-wise)
- 4. Performance of Recommender Algorithms on Top-N Recommendation Tasks --> (explicit, NNCosNgbr/PureSVD, point-wise)

Anothe axes may be around the evaluation metrics used (accuracy/error), but I am not sure yet.
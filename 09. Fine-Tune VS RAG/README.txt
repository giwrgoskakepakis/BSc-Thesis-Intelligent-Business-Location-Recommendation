This folder contains information about the comparison of the 2 approaches: fine-tuned LLM and RAG pipeline.



OLD:

The RAG pipeline had better ranking metrics (Match@3/Precision@3) than the Fine-Tuned LLM (!), but a worse BERT-score. This indicates 
that the actual top-3 suggestion is better, which is expected since it is essentially equal to the Embedder accuracy.

If I had to compare them, I would choose the RAG architecture, since:
- It requires no Fine-Tuning
- It is scalable (I can add more NACE codes without the for re-training)
- It does not hallucinate numbers
- Personalization based on the user query

However, the Fine-Tuned approach also has some advantages:
- It can generalize to NACE codes it has not seen
- It has a faster inference (no real-time embedding)
- It produces a pre-defined output (good if we want a specific format)
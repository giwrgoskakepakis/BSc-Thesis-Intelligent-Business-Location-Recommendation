This folders contains 2 files that divide the unique NACE codes in Main and Secondary. This division happens based on 
their frequency in the business entries dataset, specifically: 

- Main NACEs: frequency of 50>
- Secondary NACEs: frequency of 50<=

Both Main and Secondary NACEs will be used in the Fine-Tuning dataset so the LLM learns them all, but only the Main NACEs will
be used in the Inference dataset, since these are the most common 
from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
from peft import LoraConfig, get_peft_model, PeftModel, PeftConfig
import torch
from pathlib import Path
import json
import torch.nn.functional as F
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ollama
import traceback


app = FastAPI()


# === function that: extracts the user intent and constrains from all the messages ===   used for both approaches
def extract_intent_and_constraints(msgs, max_constraints=3, use_latest_intent=False):

    # keep only user messages
    user_texts = [m["content"].strip() for m in msgs if m.get("role") == "user" and m.get("content")]
    if not user_texts:
        return "", []

    # extract user intent:
    intent = user_texts[-1] if use_latest_intent else user_texts[0]

    # extract user constraints:
    constraints_all = user_texts[:-1] if use_latest_intent else user_texts[1:]
    constraints = constraints_all[-max_constraints:]
    return intent, constraints


# ===================================================================================================================== 
# =====================================================================================================================  Fine-Tuned LLM Approach
# =====================================================================================================================

def format_chat_prompt(system_prompt, messages):
    intent, constraints = extract_intent_and_constraints(messages)
    user_input = f"{intent}. Prefer: {'; '.join(constraints)}" if constraints else intent
    return f"<s>[INST] {user_input.strip()} [/INST]"



# -------------------------
# Fine-tuned LLM Model
# -------------------------
# actual fine-tuned model
model_name = "/home/gkakepakis/Diplomatiki/New/LLM Fine Tuning - Inference/1. LLM Fine-Tuning/LLM Models/2. 5 Epochs/fine-tuned-mistralai-Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
tokenizer.add_special_tokens({"pad_token": "[PAD]"})
tokenizer.padding_side = "right"


# Load PEFT config to find base model
peft_config = PeftConfig.from_pretrained(model_name)
base_model_name = peft_config.base_model_name_or_path

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

base_model  = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    device_map="auto",
    quantization_config=quant_config
)

# Resize to include [PAD]
base_model.resize_token_embeddings(len(tokenizer))

# Load adapter on top of resized base model
model = PeftModel.from_pretrained(base_model, model_name)

model.eval()

# Build pipeline (not used currently)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto"
)




# ===================================================================================================================== 
# =====================================================================================================================  RAG Approach
# =====================================================================================================================

# === Embed function ===
def get_embedding(text, tokenizer, model, device):
    prompt = "Represent this sentence for retrieval: " + text
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        output = model(**inputs)
        embedding = output.last_hidden_state[:, 0]
        embedding = F.normalize(embedding, p=2, dim=1)
    return embedding.cpu().numpy()[0]

# === function that: creates the LLM RAG prompt ===
def format_llm_prompt(top3_df, nace_code, nace_description, user_query=None, constraints=None):

    user_context = f'The user wants to open a business of type: "{user_query}"\n\n' if user_query else ""
    
    nace_info = f"**NACE Code: {nace_code} — {nace_description}**\n\n"
    
    neighborhood_block = "Based on data analysis, here are the top 3 recommended neighborhoods in Volos:\n\n"
    for i, row in top3_df.iterrows():
        neighborhood_block += f"{i+1}. **{row['Neighborhood']}**\n   {row['Description']}\n\n"

    instruction = (
        "Please present the 3 neighborhoods in a numbered list format like this:\n"
        "1. Neighborhood Name: Summary of strengths...\n"
        "2. Neighborhood Name: Summary of strengths...\n"
        "3. Neighborhood Name: Summary of strengths...\n\n"
        "Each point should be 2–4 sentences long, clearly explaining why the neighborhood is a good fit for the business. "
        "Avoid ranking or comparisons — describe each one positively and independently."
    )

    followup = ""
    if constraints:
        followup += ("Start your answer in a conversational tone (e.g., 'Got it, since you want…').")

    return user_context + nace_info + neighborhood_block + instruction + followup

# -------------------------
# RAG Pipeline
# -------------------------

BASE_DIR = Path("/home/gkakepakis/Diplomatiki/New/App Development")
EMB_NEIGH_DIR  = BASE_DIR / "  Neighborhood_Description_Embeddings"
EMB_NACE_DIR  = BASE_DIR / "NACE_Description_Embeddings"
NEIGH_DESC_DIR  = BASE_DIR / "Neighborhood_Descriptions"
GT_DIR   = BASE_DIR / "Ground_Truths"
NACE_DIR = BASE_DIR / "NACE_Data"

# Load the Embedder and its tokenizer
classifier_model_name = "BAAI/bge-large-en-v1.5"
classifier_tokenizer = AutoTokenizer.from_pretrained(classifier_model_name)
classifier_model = AutoModel.from_pretrained(classifier_model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
classifier_model.to(device)
classifier_model.eval()  # set eval mode
if device.type == "cuda":
    classifier_model.half()  # use FP16 for speed/memory

# Load precomputed neighborhood embeddings
with open(EMB_NEIGH_DIR / "neighborhoods_descriptions_embeddings_10.json", "r", encoding="utf-8") as f:
    precomputed_neighborhoods_embeddings = json.load(f)

# Load precomputed NACE embeddings
with open(EMB_NACE_DIR / "nace_descriptions_embeddings.json", "r", encoding="utf-8") as f:
    precomputed_nace_embeddings = json.load(f)
nace_codes = [item["nace_code"] for item in precomputed_nace_embeddings]
nace_embeddings = np.array([item["embedding"] for item in precomputed_nace_embeddings])


neighborhood_descriptions_df = pd.read_csv(NEIGH_DESC_DIR / "neighborhood_descriptions_10.csv")
top10_df = pd.read_csv(GT_DIR / "top10_final.csv")
df_naces = pd.read_csv(NACE_DIR / "unique_naces.csv")




# ===================================================================================================================== 
# =====================================================================================================================  Endpoints
# =====================================================================================================================


# -------------------------
#  Fine-Tuned LLM Endpoint
# -------------------------
@app.post("/generate_ft")
async def generate(request: Request):

    try:
        # === Extract user query from async request ===
        req = await request.json()
        system_prompt = req.get("system_prompt", "")
        messages = req.get("messages", [])

        # === Format the LLM input ===
        prompt = format_chat_prompt(system_prompt, messages)

        # --- tokenize once ---
        inputs = tokenizer(
            [prompt],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=1024,
        ).to(model.device)

        with torch.inference_mode():
            generated_ids = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False,
                use_cache=True,
            )

        # --- decode only generated part ---
        input_len = inputs["input_ids"].shape[-1]
        new_tokens = generated_ids[0][input_len:]  
        response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

        # Remove prompt prefix from response and return the response
        return {"response":  response}
    except Exception as e:
        print("❌ Internal Server Error:", e)
        traceback.print_exc()
        return {"error": str(e)}

# -------------------------
# RAG Pipeline endpoint
# -------------------------
@app.post("/generate_rag")
async def generate_rag(request: Request):

    try:
        # === Extract user query from async request ===
        req = await request.json()
        messages = req.get("messages", [])
        
        # === Extract user intent/contrains ===
        intent, constraints = extract_intent_and_constraints(messages, max_constraints=3, use_latest_intent=False)
        retrieval_text_for_rerank = (f"{intent}. Prefer: {'; '.join(constraints)}" if constraints else intent)

        # === Embed user query ===
        intent_emb  = get_embedding(intent, classifier_tokenizer, classifier_model, device)
        retrieval_emb  = get_embedding(retrieval_text_for_rerank, classifier_tokenizer, classifier_model, device)

        # === Compute cosine similarities ===
        sims = cosine_similarity([intent_emb], nace_embeddings)[0]

        # === Keep the most similar NACE code ===
        best_idx = np.argmax(sims)
        nace_code = nace_codes[best_idx]
        nace_description = df_naces[df_naces["NACE Code"] == nace_code]["Class Description"].values[0]

        # === Fetch the top 10 neighborhoods of the NACE code ===
        top10_of_nace = top10_df[top10_df['NACE Code'] == nace_code]
        top10_names = top10_of_nace.iloc[0, 1:].tolist() if not top10_of_nace.empty else []

        # === Fetch the pre-computed neighborhood embeddings ===
        top10_neighborhoods_embeddings = [
            row for row in precomputed_neighborhoods_embeddings
            if row["neighborhood"] in top10_names
        ]

        # === Create DataFrame with neighborhood: name, embedding, description ===
        top10_neighborhood_descriptions_df = pd.DataFrame([{
                "Neighborhood": row["neighborhood"],
                "Embedding": np.array(row["embedding"])
            } for row in top10_neighborhoods_embeddings
        ])
        top10_neighborhood_descriptions_df = pd.merge(top10_neighborhood_descriptions_df, neighborhood_descriptions_df, on="Neighborhood", how="left")

        # === Compute cosine similarities ===
        desc_embeddings = np.stack(top10_neighborhood_descriptions_df['Embedding'].values)
        similarities = cosine_similarity([retrieval_emb], desc_embeddings)[0]
        top10_neighborhood_descriptions_df['Similarity'] = similarities

        # === Keep the top 3 neighborhoods ===
        top3_df = top10_neighborhood_descriptions_df.sort_values(by='Similarity', ascending=False).head(3)
        top3_df = top3_df[['Neighborhood', 'Description', 'Similarity']]

        # === Construct the prompt for Llama3 ===
        prompt = format_llm_prompt(
            top3_df=top3_df,
            nace_code=nace_code,
            nace_description=nace_description,
            user_query=retrieval_text_for_rerank
        )

        # === Call Llama3 API and extract the response ===
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        return {"response": response.message.content}
    except Exception as e:
        print("❌ Internal Server Error:", e)
        traceback.print_exc()
        return {"error": str(e)}


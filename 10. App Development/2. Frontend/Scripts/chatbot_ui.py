import streamlit as st
import requests
import html
import pandas as pd
import streamlit as st
import re
from typing import List, Tuple
import pydeck as pdk

# ---------- Message render helpers ----------
def render_assistant_message(message: str) -> str:
    safe = html.escape(message).replace("\r\n", "\n").replace("\n", "<br>")
    return f"""
    <div style="background-color:#F1F0F0; border-radius:10px; padding:10px 15px; margin:8px 0; width:fit-content; max-width:80%;">
        <b>🧠 Assistant:</b><br>{safe}
    </div>
    """

def render_user_message(message: str) -> str:
    safe = html.escape(message).replace("\r\n", "\n").replace("\n", "<br>")
    return f"""
    <div style="display: flex; justify-content: flex-end;">
        <div style="background-color:#D2E3FC; border-radius:10px; padding:10px 15px; margin:8px 0; max-width:80%; text-align:left;">
            <b>👤 You:</b><br>{safe}
        </div>
    </div>
    """
# ---------- function that: extract the recommendations names from the model output ----------
def extract_neighborhood_names(reply: str, df: pd.DataFrame, k: int = 3) -> List[str]:

    reply_l = reply.lower()
    names = df["Neighborhood"].dropna().unique().tolist()

    # collect first occurrence span for each name, if any
    matches: List[Tuple[int, int, str]] = []
    for name in names:
        n_l = name.lower()
        # word-boundary-ish: avoid partial hits like "Nea" in "Neapoli"
        pattern = re.compile(rf'(?<!\w){re.escape(n_l)}(?!\w)')
        m = pattern.search(reply_l)
        if m:
            start, end = m.span()
            matches.append((start, end, name))

    # sort: by start asc, then by length desc (prefer longer when starting nearby/overlapping)
    matches.sort(key=lambda t: (t[0], -(t[1] - t[0])))

    def overlaps(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
        return not (a[1] <= b[0] or b[1] <= a[0])

    chosen_spans: List[Tuple[int, int]] = []
    chosen_names: List[str] = []

    for start, end, name in matches:
        if name in chosen_names:
            continue
        # skip if overlaps with any already chosen span
        if any(overlaps((start, end), s) for s in chosen_spans):
            continue
        chosen_spans.append((start, end))
        chosen_names.append(name)
        if len(chosen_names) >= k:
            break

    return chosen_names

# ---------- function that: creates a map visualization of the recommendations ----------
def map_visualization(reply, neighborhoods_df):
    # --- parse + order ---
    hits = extract_neighborhood_names(reply, neighborhoods_df, k=3)  # e.g. ["Epta Platania - Oksigono","Analipsi","Aivaliotika"]
    if not hits:
        st.info("No neighborhoods detected.")
        return

    sub = neighborhoods_df[neighborhoods_df["Neighborhood"].isin(hits)].copy()
    sub["__rank__"] = pd.Categorical(sub["Neighborhood"], categories=hits, ordered=True)
    sub = sub.sort_values("__rank__")

    # centroids
    pts = sub.rename(columns={"Centroid_y": "lat", "Centroid_x": "lon"})
    rank_map = {name: i + 1 for i, name in enumerate(hits)}
    pts["rank"] = pts["Neighborhood"].map(rank_map)

    # colors per rank (RGBA)
    color_map = {1: [0, 122, 255, 200], 2: [0, 200, 0, 200], 3: [255, 140, 0, 200]}
    pts["color"] = pts["rank"].map(lambda r: color_map.get(r, [120, 120, 120, 200]))

    # --- pydeck layers ---
    scatter = pdk.Layer(
        "ScatterplotLayer",
        data=pts,
        get_position="[lon, lat]",
        get_fill_color="color",
        get_radius=120,
        pickable=True,
    )
    labels = pdk.Layer(
        "TextLayer",
        data=pts,
        get_position="[lon, lat]",
        get_text="Neighborhood",
        get_size=16,   
        get_color="[30, 30, 30, 255]",
        get_text_anchor='"middle"',
        get_alignment_baseline='"top"',
        get_pixel_offset='[0, -12]', 
    )

    view = pdk.ViewState(
        longitude=float(pts["lon"].mean()),
        latitude=float(pts["lat"].mean()),
        zoom=12,
    )

    st.subheader("🗺️ Recommended neighborhoods")
    st.pydeck_chart(pdk.Deck(
        layers=[scatter, labels],
        initial_view_state=view,
        tooltip={"text": "Rank {rank}: {Neighborhood}\n{Municipal Community}"},
        map_provider="carto", 
        map_style="light" 
    ))

    # ---- table (unchanged) ----
    cols = [
        "Neighborhood","Neighborhood_Area_km2",
        "distance_to_volos_center_km","distance_to_volos_port_km",
        "dist_to_main_road_km","dist_to_bus_stop_km","dist_to_university_km"
    ]
    pretty = sub[cols].rename(columns={
        "Neighborhood": "Neighborhood",
        "Neighborhood_Area_km2": "Area (km²)",
        "distance_to_volos_center_km": "To Volos Center (km)",
        "distance_to_volos_port_km": "To Port (km)",
        "dist_to_main_road_km": "To Main Road (km)",
        "dist_to_bus_stop_km": "To Bus Stop (km)",
        "dist_to_university_km": "To University (km)",
    })
    pretty.insert(0, "Rank", range(1, len(pretty) + 1))
    pretty = pretty.reset_index(drop=True)
    fmt = {
        "Area (km²)": "{:.2f}".format,
        "To Volos Center (km)": "{:.2f}".format,
        "To Port (km)": "{:.2f}".format,
        "To Main Road (km)": "{:.2f}".format,
        "To Bus Stop (km)": "{:.2f}".format,
        "To University (km)": "{:.2f}".format,
    }
    st.dataframe(pretty.style.format(fmt), use_container_width=True)


# ---------- Different system options ----------
MODEL_OPTIONS = {
    "Fine-Tuned LLM": "http://localhost:8888/generate_ft",
    "RAG Pipeline": "http://localhost:8888/generate_rag"
}

# ---------- Neighborhood data ----------
neighborhoods_df = pd.read_csv("C:\\Users\\Giorgos\\Desktop\\HMMY\\10ο Εξάμηνο\\Διπλωματική\\3. Base Datasets\\3. Data -  Smaller Spatial Units\\1. Neighborhoods\\Extracted CSV Files\\neighborhoods_enriched.csv")


# ===================================================================================================================== 
# =====================================================================================================================  Interface
# =====================================================================================================================

# ---------- Set page and title configuration ----------
st.set_page_config(page_title="Business Chatbot", page_icon="🧠")
st.title("🤖 Business Location Chatbot Demo")

# ---------- Keep selection in session ----------
if "selected_model_name" not in st.session_state:
    st.session_state.selected_model_name = "RAG Pipeline"

# ---------- Initialize message history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Sidebar controls ----------
with st.sidebar:
    st.subheader("⚙️ Settings")
    st.session_state.selected_model_name = st.radio(
        "Model / Endpoint",
        options=list(MODEL_OPTIONS.keys()),
        index=list(MODEL_OPTIONS.keys()).index(st.session_state.selected_model_name),
        horizontal=False,
        help="Choose which backend endpoint to call for responses.",
    )

    st.caption(f"Current endpoint: `{MODEL_OPTIONS[st.session_state.selected_model_name]}`")

    if st.button("🧹 Clear chat"):
        st.session_state.messages = []
        st.rerun()


# ---------- Assistant greeting on first load ----------
if len(st.session_state.messages) == 0:
    greeting = "Hello! I'm here to help you find the optimal location for a new business in Volos. Ask me anything!"
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# ---------- Avatars ----------
USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

#  ----------Default system prompt ----------
SYSTEM_PROMPT = "You are a helpful assistant that suggests optimal business locations in Greece based on demographics and area characteristics."

# ---------- Display previous messages (every time we send a new message) ----------
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        st.markdown(render_user_message(content), unsafe_allow_html=True)
    else:
        st.markdown(render_assistant_message(content), unsafe_allow_html=True)

# ---------- Input box for the user ----------
user_input = st.chat_input("Ask your business location question...")


# ---------- Triggered when the user sends a new message ----------
if user_input:

    # === 1. Add new user message to history ===
    st.session_state.messages.append({"role": "user", "content": user_input})

    # === 2. Immediately show the user message and a placeholder for the assistant (visual trick) ===
    with st.container():
        st.markdown(render_user_message(user_input), unsafe_allow_html=True)
        bot_placeholder = st.empty()  # Reserve space for later assistant response

    # === 3. Create request payload ===
    payload = {
        "system_prompt": SYSTEM_PROMPT,
        "messages": st.session_state.messages
    }

    # === 4. Send to backend (with spinner for user inference) ===
    with st.spinner("Generating response..."):
        try:

            # extract selected model endpoint
            endpoint = MODEL_OPTIONS[st.session_state.selected_model_name]

            # send request to backend
            res = requests.post(endpoint, json=payload, timeout=120)
            res.raise_for_status()

            # get reply from backend
            reply = (res.json() or {}).get("response", "")
            reply = (reply or "").strip() or "⚠️ Empty response from server."

            # display a map visualization
            map_visualization(reply, neighborhoods_df)

        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

    # === 5. Display the assistant reply in the placeholder ===
    bot_placeholder.markdown(render_assistant_message(reply), unsafe_allow_html=True)

    # === 6. Add new assistant message to chat history ===
    st.session_state.messages.append({"role": "assistant", "content": reply})
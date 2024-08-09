import streamlit as st
from PIL import Image
from fpdf import FPDF
import os
import time
import random

# Constants
CARD_WIDTH_INCH = 2.48
CARD_HEIGHT_INCH = 3.46
A4_WIDTH_INCH = 8.27
A4_HEIGHT_INCH = 11.69
DPI = 300

# Calculate sizes in points (1 inch = 72 points)
CARD_WIDTH_PT = CARD_WIDTH_INCH * 72
CARD_HEIGHT_PT = CARD_HEIGHT_INCH * 72
A4_WIDTH_PT = A4_WIDTH_INCH * 72
A4_HEIGHT_PT = A4_HEIGHT_INCH * 72

# Margins and spacing
MARGIN_PT = 36  # 0.5 inch margin
SPACING_PT = 18  # 0.25 inch spacing
TEXT_MARGIN_PT = 6  # Space above the image for the filename

# Number of cards per row and column
CARDS_PER_ROW = 3
CARDS_PER_COLUMN = 3

def create_pdf(images, output_pdf):
    # Create PDF object
    pdf = FPDF('P', 'pt', (A4_WIDTH_PT, A4_HEIGHT_PT))
    pdf.set_font("Arial", size=8)

    # Calculate the total content width and height
    total_content_width = (CARD_WIDTH_PT * CARDS_PER_ROW) + (SPACING_PT * (CARDS_PER_ROW - 1))
    total_content_height = (CARD_HEIGHT_PT * CARDS_PER_COLUMN) + (SPACING_PT * (CARDS_PER_COLUMN - 1))

    # Calculate the starting margins to center the cards
    start_margin_x = (A4_WIDTH_PT - total_content_width) / 2
    start_margin_y = (A4_HEIGHT_PT - total_content_height) / 2

    # Process images in chunks of 9
    for i in range(0, len(images), 9):
        pdf.add_page()
        chunk = images[i:i + 9]
        for j, image_file in enumerate(chunk):
            img = Image.open(image_file)
            img = img.resize((int(CARD_WIDTH_INCH * DPI), int(CARD_HEIGHT_INCH * DPI)), Image.LANCZOS)

            x_pt = start_margin_x + (j % CARDS_PER_ROW) * (CARD_WIDTH_PT + SPACING_PT)
            y_pt = start_margin_y + (j // CARDS_PER_ROW) * (CARD_HEIGHT_PT + SPACING_PT)

            # Add the filename text above the image, closer to the image
            text_x_pt = x_pt
            text_y_pt = y_pt - TEXT_MARGIN_PT
            pdf.text(text_x_pt, text_y_pt, os.path.splitext(image_file.name)[0])

            # Save temporary image to avoid format issues
            temp_image = f"temp_{i}_{j}.png"
            img.save(temp_image, dpi=(DPI, DPI))

            # Add image to PDF
            pdf.image(temp_image, x_pt, y_pt, CARD_WIDTH_PT, CARD_HEIGHT_PT)

            # Remove temporary image
            os.remove(temp_image)

    # Save the PDF to a temporary file
    temp_pdf_path = "output.pdf"
    pdf.output(temp_pdf_path, 'F')

    # Read the PDF file as bytes
    with open(temp_pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # Remove the temporary PDF file
    os.remove(temp_pdf_path)

    return pdf_bytes

# Define a simple Pokémon class
class Pokemon:
    def __init__(self, name, hp, attack, attack_name):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.attack_name = attack_name

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_fainted(self):
        return self.hp == 0

# Define Pokémon and Easter Eggs
pokemon_list = [
    Pokemon(name="Pikachu", hp=100, attack=20, attack_name="Thunderbolt"),
    Pokemon(name="Charizard", hp=120, attack=25, attack_name="Flamethrower"),
    Pokemon(name="Squirtle", hp=90, attack=18, attack_name="Water Gun"),
    Pokemon(name="Bulbasaur", hp=100, attack=15, attack_name="Vine Whip"),
    Pokemon(name="Jigglypuff", hp=80, attack=10, attack_name="Sing"),
    Pokemon(name="Mewtwo", hp=150, attack=30, attack_name="Psychic")
]

easter_eggs = [
    Pokemon(name="Space Marine", hp=200, attack=50, attack_name="Bolter"),
    Pokemon(name="Gandalf", hp=180, attack=40, attack_name="You Shall Not Pass"),
    Pokemon(name="Sauron", hp=250, attack=60, attack_name="Mace of Doom")
]

# Function to randomly choose an Easter Egg character with a small chance
def random_easter_egg():
    if random.random() < 0.05:  # 5% chance to trigger an Easter Egg
        return random.choice(easter_eggs)
    return None

# Streamlit app
st.set_page_config(
    page_title="Card Proxy PDF Generator & Pokémon Battle",
    page_icon="🎴",
    layout="wide",
)

# Custom CSS for minimalistic design
st.markdown("""
<style>
    .stApp {
        background-color: #f7f7f7;
        color: #333333;
    }
    h1, h3 {
        color: #666666;
    }
    .stButton>button {
        background-color: #999999;
        color: #ffffff;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #777777;
        transform: scale(1.05);
    }
    .stDownloadButton>button {
        background-color: #555555;
        color: #ffffff;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stDownloadButton>button:hover {
        background-color: #333333;
        transform: scale(1.05);
    }
    hr {
        border: none;
        height: 1px;
        background-color: #cccccc;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Card Proxy PDF Generator</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Create Your Own Pokémon or MTG Proxies and Battle Pokémon!</h3>", unsafe_allow_html=True)

# Upload PNG or JPG files
uploaded_files = st.file_uploader("Choose PNG or JPG files", accept_multiple_files=True, type=["png", "jpg"])

if uploaded_files:
    if st.button("Generate PDF"):
        with st.spinner('Generating PDF...'):
            pdf_bytes = create_pdf(uploaded_files, "pdf_cards_a4.pdf")
            time.sleep(2)  # Simulate progress

        st.success("PDF generated successfully!")
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="pdf_cards_a4.pdf",
            mime="application/pdf"
        )

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <p style='text-align: center;'>
    <strong>Note:</strong> The images will be printed at their actual card size, so make sure your images are at least 300 DPI 
    for the best results.
    </p>
    """,
    unsafe_allow_html=True
)

# Secret Pokémon Battle Button
if st.button("DON'T CLICK ME"):
    st.session_state.show_battle = True

# Check if the battle game should be shown
if st.session_state.get("show_battle", False):
    st.markdown("<h3 style='text-align: center;'>Pokémon Battle Game</h3>", unsafe_allow_html=True)

    if "game_started" not in st.session_state:
        st.session_state.game_started = False
        st.session_state.player_pokemon = None
        st.session_state.enemy_pokemon = None

    if not st.session_state.game_started:
        player_choice = st.selectbox("Choose your Pokémon", [p.name for p in pokemon_list])
        if st.button("Start Battle"):
            st.session_state.player_pokemon = next(p for p in pokemon_list if p.name == player_choice)
            st.session_state.enemy_pokemon = random_easter_egg() or random.choice(pokemon_list)
            st.session_state.game_started = True
            st.session_state.player_hp = st.session_state.player_pokemon.hp
            st.session_state.enemy_hp = st.session_state.enemy_pokemon.hp
            st.write(f"A wild {st.session_state.enemy_pokemon.name} appeared!")
    else:
        player_pokemon = st.session_state.player_pokemon
        enemy_pokemon = st.session_state.enemy_pokemon

        st.write(f"**{player_pokemon.name}** HP: {st.session_state.player_hp}")
        st.write(f"**{enemy_pokemon.name}** HP: {st.session_state.enemy_hp}")

        if st.session_state.player_hp > 0 and st.session_state.enemy_hp > 0:
            if st.button(f"Attack with {player_pokemon.attack_name}"):
                # Player attacks the enemy Pokémon
                enemy_damage = random.randint(5, player_pokemon.attack)
                enemy_pokemon.take_damage(enemy_damage)
                st.session_state.enemy_hp = enemy_pokemon.hp
                st.write(f"{player_pokemon.name} dealt {enemy_damage} damage to {enemy_pokemon.name}!")

                # Enemy Pokémon counterattacks
                if not enemy_pokemon.is_fainted():
                    player_damage = random.randint(5, enemy_pokemon.attack)
                    player_pokemon.take_damage(player_damage)
                    st.session_state.player_hp = player_pokemon.hp
                    st.write(f"{enemy_pokemon.name} dealt {player_damage} damage to {player_pokemon.name}!")

        if enemy_pokemon.is_fainted():
            st.success(f"You defeated the wild {enemy_pokemon.name}!")
        elif player_pokemon.is_fainted():
            st.error(f"Your {player_pokemon.name} fainted!")

        if st.session_state.player_hp <= 0 or st.session_state.enemy_hp <= 0:
            if st.button("Play Again"):
                st.session_state.game_started = False
                st.session_state.player_hp = 0
                st.session_state.enemy_hp = 0

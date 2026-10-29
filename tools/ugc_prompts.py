import json
# name, age, face, outfit, setting, action(video)
P=[
("Marta",57,"oval face, soft jawline, warm olive Mediterranean skin, dark brown eyes with fine crow's feet when she smiles, natural thick eyebrows with a few grey hairs, shoulder-length chestnut hair with visible grey roots pulled into a loose low bun, small gold stud earrings",
 "plain grey crew-neck sweatshirt","small real Italian kitchen in the morning, moka pot on the stove, window light from the side",
 "she smiles at the camera, tears the top corner of the sachet, drinks it in one go, then nods with a satisfied little laugh"),
("Paola",62,"round face, full cheeks, fair skin with a few light freckles and faint sun spots on the cheekbones, light hazel eyes, soft laugh lines, short silver-grey pixie cut, thin red-framed reading glasses pushed up on her head",
 "navy blue high-neck knit pullover","bright living room with a bookshelf and a plant behind her, afternoon light",
 "she talks to the camera enthusiastically, shows the sachet close to the lens, then drinks it and gives a thumbs up"),
("Silvia",59,"long face with high cheekbones, light tan skin, green-grey eyes, gentle smile lines, straight dark-blonde bob with natural grey strands at the temples, no earrings",
 "beige zip-up fleece closed up to the neck","sitting in the driver's seat of a parked car, daylight through the windshield, seatbelt off",
 "she holds the sachet toward the lens, laughs, tears it open and sips it, then shrugs happily as if saying 'that's it'"),
("Elena",56,"heart-shaped face, medium olive skin, almond dark eyes, defined brows, faint expression lines on the forehead, wavy dark brown hair just past the shoulders with a few grey strands, small hoop earrings",
 "white cotton crew-neck t-shirt under an open denim shirt buttoned high","bedroom vanity corner with a round mirror behind her, morning light",
 "she taps the sachet with her fingernail, smiles, tears it and drinks it, then touches her cheek lightly with her fingertips"),
("Cristina",64,"square face, strong jaw, fair rosy skin, blue eyes with soft crow's feet, short wavy white-silver hair with a side part, small pearl earrings",
 "pale pink turtleneck sweater","cozy sofa in a living room with a cream throw blanket, lamp light and window light mixed",
 "she speaks to the camera like a friend, raises the sachet next to her face, then drinks it and smiles warmly"),
("Valentina",61,"oval face with a slightly pointed chin, medium tan skin, dark brown eyes, softly defined smile lines, shoulder-length auburn dyed hair with a slightly grown-out root, tortoiseshell glasses",
 "mustard yellow crew-neck cardigan buttoned to the top","home office desk with a laptop and a mug, window behind her slightly overexposed",
 "she pushes her glasses up, shows the sachet to the camera, drinks it and raises her eyebrows with a pleased expression"),
("Anna",63,"round face, deep olive Southern Italian skin, very dark eyes, thick dark eyebrows, laugh lines around the mouth, chin-length black hair with a white streak at the front, small gold cross necklace over her top",
 "black high-neck long-sleeve top","sunny balcony with terracotta pots and geraniums, outdoor daylight",
 "she laughs, holds the sachet up against the sky, then tears and drinks it and blows a playful kiss to the camera"),
("Federica",58,"long oval face, fair skin with a few freckles on the nose, light brown eyes, fine lines under the eyes, long straight light-brown hair with natural grey threads tied in a ponytail",
 "olive green crew-neck sweatshirt","garden bench with hedges and a wooden fence behind, soft overcast daylight",
 "she walks a couple of steps holding the phone, sits, shows the sachet, drinks it and smiles with closed lips"),
("Roberta",60,"wide face with soft features, light olive skin, hazel eyes, gentle crow's feet, short layered salt-and-pepper hair, small silver earrings",
 "light blue denim shirt buttoned to the collar","kitchen counter with a fruit bowl and a cutting board, warm morning light",
 "she cuts to the chase: shows the sachet, squeezes it, drinks it and gives a decisive nod to the camera"),
("Simona",61,"heart-shaped face, warm beige skin, green eyes, subtle laugh lines, voluminous curly dark-blonde hair with grey at the hairline, red lipstick",
 "cream high-neck ribbed sweater","sitting at a cafe table outdoors in an Italian piazza, cappuccino cup on the table, daylight",
 "she looks around then to the camera with a conspiratorial smile, takes the sachet out of her bag, drinks it and winks"),
("Daniela",55,"oval face, medium olive skin, dark brown eyes, defined brows, only very fine lines at the eye corners, long dark brown hair with soft waves, no visible grey, small gold hoops",
 "lilac crew-neck t-shirt under a light grey zip hoodie zipped up","bathroom with white tiles and a towel on a hook behind her, bright morning light",
 "she finishes applying lip balm, picks up the sachet, shows it, drinks it and smiles brightly"),
("Chiara",65,"slim oval face, fair skin with a few age spots on the temples, light blue eyes, elegant crow's feet, chin-length straight snow-white bob, thin gold-rimmed glasses",
 "camel-colour mock-neck sweater","bright dining room with a vase of fresh flowers on the table, window light",
 "she smiles serenely, shows the sachet close to the lens, tears it, drinks it slowly and nods as if approving the taste"),
]
SACHET="The sachet is identical to the reference image: white pouch, black lowercase 'within' logo, orange 'FORMULATED FOR YOU', 'Mango Passionfruit'."
def frame(p):
    n,a,face,outfit,setting,_=p
    return (f"Vertical 9:16 still from a real TikTok video, shot on a smartphone front camera at arm's length, handheld, slightly wide-angle. "
      f"A real Italian woman, exactly {a} years old: {face}. She wears a {outfit}; fully covered neckline, no cleavage. Setting: {setting}. "
      f"She is mid-sentence talking to the camera, holding the white Within sachet from the reference next to her face, label facing the lens. "
      f"Her skin looks remarkably youthful for {a}: firm, plump, even-toned, hydrated and luminous, with a healthy glow — yet it is unmistakably real: visible pores, natural texture, real fine lines consistent with her age, no wrinkles smoothed away. "
      f"She clearly looks over 50, just glowing and well. Minimal makeup, no beauty filter, no airbrushing, no retouching, not a model, ordinary everyday person, candid natural expression. "
      f"Natural available light, real unstyled lived-in home, slight motion blur, smartphone image noise, authentic creator content look, no text overlays. {SACHET}")
def video(p):
    n,a,face,outfit,setting,act=p
    return (f"Authentic TikTok creator video, vertical, filmed with a smartphone front camera held at arm's length, natural handheld shake, real sponsored-UGC feel. "
      f"Same woman as the start image, {a} years old, keep her face, hair, glasses, skin and outfit exactly as in the start image: {face}. "
      f"Action: {act}. She talks naturally to the camera between actions with relaxed real expressions. "
      f"Her skin stays realistic with visible pores and age-appropriate fine lines, youthful firm glowing complexion, no smoothing, no beauty filter, no face morphing. "
      f"Natural light, no color grading, no text, no subtitles, no music. {SACHET}")
json.dump([{"name":p[0],"age":p[1],"frame":frame(p),"video":video(p)} for p in P],open(__file__.replace('.py','.json'),'w'),ensure_ascii=False,indent=1)
print(len(P)); print(frame(P[0])); print(video(P[0]))

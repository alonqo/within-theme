import json,os
D=os.path.dirname(os.path.abspath(__file__))
old=json.load(open(os.path.join(D,'ugc_prompts.json')))
_ns={};exec(open(os.path.join(D,'ugc_prompts.py')).read().split('SACHET=')[0],_ns);P=_ns['P']
# per-woman: (format label, framing for still, action for video, outfit override or None)
F={
"Marta":("phone propped on the kitchen counter, static wide shot, morning routine",
  "the phone is propped up on the kitchen counter filming her from waist up, she is not looking at the camera, busy making coffee with a moka pot; a Within sachet lies on the counter next to the coffee cups",
  "static propped-phone shot: she pours coffee, picks up the Within sachet from the counter, tears it and drinks it while the moka gurgles, then glances at the camera and smiles as if caught in the act"),
"Paola":("GRWM at the bathroom mirror, phone propped on the shelf",
  "get-ready-with-me: phone propped on the bathroom shelf, she faces the camera while patting moisturiser onto her cheeks, toiletries and the Within sachet on the sink edge in front of her",
  "GRWM: she pats moisturiser on her face talking to the camera, then picks up the Within sachet from the sink, drinks it as one step of the routine and continues patting her cheeks"),
"Silvia":("phone on a car dashboard mount",
  "phone fixed on the car dashboard holder filming her from the passenger side angle, she sits in the driver's seat of a parked car with her handbag on her lap, a Within sachet in her hand, glancing at the camera while talking",
  "dashboard-mount shot: she talks to the camera while putting on her seatbelt, drinks the Within sachet quickly, throws the empty sachet into the cup holder and gets ready to drive off"),
"Elena":("unboxing on a table, phone propped",
  "unboxing video: phone propped on a wooden table, she sits behind the white Within box and is opening it, pulling out the sachets, looking down at the box with curiosity",
  "unboxing: she opens the Within box, lifts out a row of sachets and fans them out to the camera, reads the back, tears one open and tastes it, then raises her eyebrows positively"),
"Cristina":("skin close-up by the window, handheld",
  "very close handheld front-camera shot by a bright window, her face fills most of the frame as she shows her skin in daylight, fingertips lightly touching her cheekbone; a Within sachet is visible on the windowsill in the background",
  "skin check: she moves the phone closer and turns her face in the window light, touching her cheek and jawline to show her skin, then reaches to the windowsill, shows the Within sachet briefly and smiles"),
"Valentina":("walking vlog outdoors, handheld",
  "day-in-my-life walking vlog: handheld front camera while she walks along a tree-lined Italian street in autumn with a tote bag on her shoulder, talking to the camera",
  "walking vlog: she walks talking to the camera, stops by a bench, takes a Within sachet out of her tote bag, drinks it on the go and keeps walking, smiling"),
"Anna":("lifestyle on the balcony, phone propped on the table",
  "phone propped on a small balcony table filming her from a distance, she is watering geraniums in terracotta pots, a glass of water and a Within sachet on the table in the foreground",
  "propped-phone lifestyle shot: she waters the plants, then comes back to the table, picks up the Within sachet, drinks it, wipes her lips and laughs toward the camera"),
"Federica":("after a garden workout, phone on the ground",
  "phone propped low on the grass filming her sitting on a yoga mat in the garden after stretching, slightly out of breath, a water bottle and a Within sachet beside the mat",
  "post-workout: she finishes a stretch, sits cross-legged on the mat, grabs the Within sachet, drinks it and gives a relaxed thumbs up to the camera"),
"Roberta":("filmed by her daughter, candid",
  "candid shot filmed by someone else standing across the kitchen (her daughter), Roberta is at the counter laughing and pointing at the camera telling her to stop filming, holding a Within sachet",
  "filmed by a family member: Roberta laughs and tells the person filming to stop, then gives in, drinks the Within sachet and jokingly shows the empty sachet to the camera"),
"Simona":("cafe table, phone propped against the sugar jar",
  "phone propped against the sugar jar on an outdoor cafe table in an Italian piazza, medium shot, she is chatting to the camera with a cappuccino, a Within sachet lying next to the saucer",
  "cafe chat: she talks to the camera with animated gestures, sips her cappuccino, then picks up the Within sachet from the table, drinks it and winks"),
"Daniela":("GRWM bathroom morning, phone propped on the sink",
  "get-ready-with-me in a white-tiled bathroom: phone propped on the sink, she is brushing her long hair while talking to the camera, the Within sachet on the sink edge",
  "GRWM: she brushes her hair talking to the camera, puts the brush down, drinks the Within sachet and goes back to doing her hair, smiling"),
"Chiara":("story-time on the sofa, phone on a tripod",
  "story-time video: phone on a small tripod filming her sitting on a sofa in a bright living room, medium shot, she is telling a story with her hands, a box of Within sachets on the coffee table in front of her",
  "story time: she tells a story to the camera with expressive hands, leans forward, takes a Within sachet from the box on the coffee table, drinks it and nods approvingly"),
}
SACHET="The sachet/box is identical to the reference image: white pouch, black lowercase 'within' logo, orange 'FORMULATED FOR YOU', 'Mango Passionfruit'."
SKIN=lambda a:(f"She is exactly {a} years old and clearly over 50; her skin looks remarkably youthful for her age: firm, even-toned, hydrated and luminous, yet real with visible pores and natural fine lines, no airbrushing, no beauty filter. ")
out=[]
for o,(n,a,face,outfit,setting,_) in zip(old,P):
    fmt,still,act=F[n]
    fr=(f"Vertical 9:16 still frame from a real TikTok video, format: {fmt}. Same woman as the first reference image (keep her exact face, hair and features): {face}. "
        f"She wears a {outfit}; covered neckline, no cleavage. Scene: {still}. "+SKIN(a)+
        "Ordinary everyday person, not a model, candid real expression, natural light, real unstyled environment, smartphone image quality with slight noise, no text overlays, no captions. "+SACHET)
    vd=(f"Authentic TikTok video, vertical, format: {fmt}. Same woman as the start image, {a} years old, keep her face, hair, skin and outfit exactly as in the start image. "
        f"Action: {act}. Natural real movements and expressions, not an advert, not a spokesperson. "
        "Realistic skin with pores and age-appropriate fine lines, youthful glowing complexion, no smoothing, no face morphing. Natural light, no color grading, no text, no subtitles, no music. "+SACHET)
    out.append({"name":n,"age":a,"format":fmt,"old_frame":o['frame_job'],"frame":fr,"video":vd})
json.dump(out,open(os.path.join(D,'ugc_v2.json'),'w'),ensure_ascii=False,indent=1)
print(out[0]['frame']);print(out[0]['video'])

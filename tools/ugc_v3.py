import json,os
D=os.path.dirname(os.path.abspath(__file__))
v2=json.load(open(os.path.join(D,'ugc_v2.json')))
# extra amateur details per woman: (mess/background, imperfection, camera angle)
X={
"Marta":("dish rack full of mugs, a tea towel thrown on the counter, phone charger cable, fridge covered in magnets and kids' drawings","a few loose strands of hair out of the bun, no makeup at all","phone leaning against the backsplash at a slightly crooked angle, her head partly cut off at the top of the frame"),
"Paola":("cluttered bathroom shelf with half-used bottles, toothbrush cup, hair dryer on the counter, a towel hanging crooked","bare face with moisturiser not fully rubbed in","phone propped low on the shelf so the camera looks slightly up at her"),
"Silvia":("parking ticket and sunglasses on the dashboard, receipts in the door pocket, a water bottle on the passenger seat","hair a bit flat from the day","dashboard holder angle from below, windshield glare blowing out part of the frame"),
"Elena":("kitchen table with a fruit bowl, mail, reading glasses and a phone case, unmade chairs","hair loosely clipped up, no makeup","phone propped against a mug, framing a bit too low so the table takes half the frame"),
"Cristina":("plain white curtain and a radiator behind her","no makeup, a few stray hairs","extremely close and slightly off-centre, part of her forehead cut off, front camera wide-angle"),
"Valentina":("ordinary residential street with parked cars and scooters, autumn leaves on the pavement","glasses slightly crooked, hair moved by the wind","arm's-length shot bouncing with her steps, horizon tilted"),
"Anna":("small cramped balcony with a drying rack of laundry, plastic chairs, a watering can","hair messy from the wind","phone propped on the plastic table far away, she is small in the frame"),
"Federica":("ordinary back garden with patchy grass, a plastic garden chair and a hose","face a little flushed and shiny from exercise, hair coming out of the ponytail","phone propped on the grass at a low angle, slightly crooked"),
"Roberta":("busy home kitchen with pans on the stove, a cluttered counter, a calendar on the wall","no makeup, apron over her shirt","filmed by someone else with the rear camera, shaky, slightly out of focus at first, someone's thumb at the corner of the frame"),
"Simona":("ordinary bar terrace with metal chairs, napkin dispenser, other customers blurred in the background","hair frizzy from humidity","phone leaning on the sugar jar, tilted, framing her slightly off-centre"),
"Daniela":("small bathroom with mismatched towels, a laundry basket, products crowded on the sink","hair still slightly damp, no makeup","phone propped on the sink looking up at her, mirror reflection partly visible"),
"Chiara":("lived-in living room with a crocheted blanket, family photos, a TV remote and reading glasses case on the coffee table","no makeup except a little lipstick","cheap tripod placed slightly too low, frame a bit crooked"),
}
UGC=("Make it look like a raw, unedited frame grab from a real amateur TikTok filmed on an ordinary smartphone by a normal person, NOT a photoshoot and NOT an advert: "
 "flat phone-camera HDR look, slightly blown-out window highlights, mixed warm/cool white balance, mild compression artifacts and noise, everything in focus (no bokeh, no shallow depth of field), "
 "imperfect amateur framing, real clutter in the background, nothing styled, no studio or cinematic lighting.")
out=[]
for x in v2:
    n=x['name'];bg,imp,cam=X[n]
    fr=(f"Edit the first reference image. Keep exactly the same woman (same face, hair, age {x['age']}, outfit, covered neckline) and the same kind of scene and action. "
        f"{UGC} Camera: {cam}. Background: {bg}. Her look: {imp}. "
        f"Her skin stays real with visible pores and natural fine lines for a {x['age']}-year-old, but firm, even-toned and with a healthy glow; no retouching, no beauty filter. "
        "Keep the Within sachet as in the second reference image: white pouch, black lowercase 'within' logo, orange 'FORMULATED FOR YOU', 'Mango Passionfruit'. No text overlays.")
    act=x['video'].split('Action: ')[1].split(' Natural real movements')[0]
    vd=(f"Raw amateur TikTok clip filmed on an ordinary smartphone by a normal Italian woman, {x['age']} years old, NOT an advert, NOT cinematic. Same woman, same scene and framing as the start image. "
        f"Action: {act} She talks casually, mid-sentence, with real unpolished gestures, glances at the phone screen to check herself, small awkward pauses. "
        "Camera behaviour: phone-camera auto-exposure and white balance shifting slightly, small focus hunting, natural shake if handheld or tiny wobble if propped, 30fps phone look, mild compression. "
        "No smooth camera moves, no gimbal, no dolly, no bokeh, no colour grading, no beauty filter, no face morphing; realistic skin with pores and fine lines. No text, no subtitles, no music. "
        "Within sachet as in the reference image: white pouch, black lowercase 'within' logo, orange 'FORMULATED FOR YOU', 'Mango Passionfruit'.")
    out.append(dict(name=n,age=x['age'],v2_frame=x['frame_job'],frame=fr,video=vd))
json.dump(out,open(os.path.join(D,'ugc_v3.json'),'w'),ensure_ascii=False,indent=1)
print(out[0]['frame']);print();print(out[0]['video'])

import json,os,re
D=os.path.dirname(os.path.abspath(__file__))
v3=json.load(open(os.path.join(D,'ugc_v3.json')))
src=open(os.path.join(D,'ugc_v3.py')).read()
ns={};exec(src[src.index('X={'):src.index('UGC=(')],ns);X=ns['X']
HAIR={"Marta":"glossy warm chestnut-brown hair, shoulder length, freshly blow-dried",
"Paola":"honey-blonde chin-length bob, nicely styled",
"Silvia":"golden-blonde shoulder-length hair with soft waves",
"Elena":"glossy dark-brown wavy hair past the shoulders",
"Cristina":"chic ash-blonde short layered haircut",
"Valentina":"rich copper-auburn shoulder-length hair, freshly coloured",
"Anna":"glossy jet-black chin-length bob",
"Federica":"long caramel-brown hair in a sleek ponytail",
"Roberta":"short chestnut pixie cut with caramel highlights",
"Simona":"voluminous dark-blonde curls",
"Daniela":"long dark-brown hair in soft waves",
"Chiara":"elegant champagne-blonde bob"}
BASE={0:'8aab3fd7-7843-4bbc-be0a-cbfbe9efb8bf',4:'12af5abf-02c3-4cd1-bb95-2bbdd8c15388',8:'a51ddb99-7b5c-472d-b3f1-8486d2fac046'}
UGC=("The image must stay a raw, unedited frame grab from a real amateur TikTok filmed on an ordinary smartphone, NOT a photoshoot and NOT an advert: flat phone-camera HDR look, slightly blown-out highlights, mixed white balance, mild noise and compression, everything in focus (no bokeh), imperfect amateur framing, real lived-in clutter, no studio or cinematic lighting.")
out=[]
for i,x in enumerate(v3):
    n=x['name'];a=x['age'];bg,_,cam=X[n]
    fr=(f"Edit the first reference image: keep the same scene, location, clutter, camera angle, framing, outfit (covered neckline, no cleavage) and action. "
        f"Change the woman into a beautiful, attractive, elegant Italian lady aged {a}: {HAIR[n]}, absolutely no grey or white hair anywhere, well-groomed, shaped eyebrows, light natural everyday makeup (a little mascara, soft blush, tinted lip balm), bright eyes, warm smile. "
        f"She still clearly looks in her {('fifties' if a<60 else 'sixties')} with a few soft fine lines, but her skin is firm, smooth, even-toned and glowing, visibly youthful for her age; real skin texture with pores, no airbrushing, no beauty filter. "
        f"{UGC} Camera: {cam}. Background: {bg}. "
        "Keep the Within sachet as in the second reference image: white pouch, black lowercase 'within' logo, orange 'FORMULATED FOR YOU', 'Mango Passionfruit'. No text overlays.")
    vd=x['video'].replace("realistic skin with pores and fine lines.","realistic skin with pores and soft fine lines, beautiful well-groomed woman, no grey or white hair.")
    if n=="Roberta":
        vd=("Raw amateur clip filmed on an ordinary smartphone by her daughter, the woman is 60 years old, NOT an advert, NOT cinematic. Same woman, same scene and framing as the start image. "
            "Action: she laughs and tells the person filming to stop, waves her hand at the lens, then gives in, drinks the Within sachet and jokingly shows the empty sachet to the camera. Real unpolished gestures, genuine laughter, small awkward pauses. "
            "Camera behaviour: handheld by someone else, shaky, phone auto-exposure and white balance shifting slightly, small focus hunting, 30fps phone look, mild compression. "
            "No smooth camera moves, no gimbal, no bokeh, no colour grading, no beauty filter, no face morphing; realistic skin with pores and soft fine lines, beautiful well-groomed woman, no grey or white hair. No text, no subtitles, no music. "
            "Within sachet as in the reference image: white pouch, black lowercase 'within' logo, orange 'FORMULATED FOR YOU', 'Mango Passionfruit'.")
    out.append(dict(name=n,age=a,base=BASE.get(i,x['v2_frame']),frame=fr,video=vd))
json.dump(out,open(os.path.join(D,'ugc_v4.json'),'w'),ensure_ascii=False,indent=1)
print(json.dumps([{'index':i,'params':{'model':'nano_banana_2_1','prompt':o['frame'],'aspect_ratio':'9:16','resolution':'2k','medias':[{'value':o['base'],'role':'image_references'},{'value':'d1c7b637-a322-4ef6-9c87-3d51c3bdfc56','role':'image_references'}]}} for i,o in enumerate(out)],ensure_ascii=False))

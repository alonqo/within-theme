import json,os
D=os.path.dirname(os.path.abspath(__file__))
v4=json.load(open(os.path.join(D,'ugc_v4.json')))
W={
"Marta":"a large bright kitchen in an elegant Italian home: white marble island, brass taps, fresh flowers in a vase, a few everyday things left around (keys, a phone, a fruit bowl)",
"Paola":"an elegant marble bathroom with a double vanity, brass taps, fluffy white towels, perfume bottles and skincare jars on a tray",
"Silvia":"the interior of an expensive car with cream leather seats and wooden trim (no visible brand logos), a designer leather handbag on her lap, sunglasses on the dashboard",
"Elena":"an elegant apartment dining table with herringbone parquet floor, a designer pendant lamp, a vase of peonies, mail and reading glasses on the table",
"Cristina":"a tall window with sheer linen curtains in an elegant city apartment, terracotta rooftops of an Italian city visible outside",
"Valentina":"an elegant Italian city-centre street with boutiques and cafés, she carries a leather tote and a paper shopping bag",
"Anna":"a large terrace with a sea view, rattan furniture with linen cushions, lemon trees in big terracotta pots",
"Federica":"the manicured garden of a villa with a swimming pool and olive trees in the background, yoga mat on a teak deck",
"Roberta":"a large elegant country-house kitchen with marble counters, copper pans hanging, a big wooden table with bread and fruit",
"Simona":"a café terrace at an elegant marina with sailing yachts in the background, white tablecloth, cappuccino in a fine cup",
"Daniela":"an elegant bathroom with a walk-in shower, marble walls, a wide mirror and nice skincare bottles on the vanity",
"Chiara":"an elegant living room with a linen sofa, framed art on the walls, a grand piano, a marble fireplace and a coffee table with art books",
}
out=[]
for x in v4:
    n=x['name'];a=x['age']
    fr=(f"Edit the first reference image: keep exactly the same woman (same face, same hair colour and cut, age {a}, light makeup, no grey hair), the same action, pose and the same amateur phone-camera framing and angle. "
        f"Change the setting to a wealthy, upscale lifestyle: {W[n]}. Upgrade her outfit to quietly luxurious clothes (fine cashmere or silk, high or crew neckline, no cleavage), delicate gold jewellery, manicured nails. "
        "It must still look like a real, unedited frame grab from an amateur TikTok filmed on a smartphone by the woman herself (or a family member): phone-camera HDR look, slightly blown highlights, mild noise, everything in focus, no bokeh, imperfect framing, real lived-in details, not a photoshoot, not an advert, not staged. "
        f"Skin: real texture with pores and soft fine lines for a {a}-year-old, firm, glowing, youthful for her age, no airbrushing. "
        "Keep the Within sachet as in the second reference image: white pouch, black lowercase 'within' logo, orange 'FORMULATED FOR YOU', 'Mango Passionfruit'. No text overlays.")
    vd=x['video'].replace("NOT an advert, NOT cinematic.","NOT an advert, NOT cinematic, wealthy elegant lifestyle at home.")
    out.append(dict(name=n,age=a,base=x['frame_job'],frame=fr,video=vd))
json.dump(out,open(os.path.join(D,'ugc_v5.json'),'w'),ensure_ascii=False,indent=1)
print(json.dumps([{'index':i,'params':{'model':'nano_banana_2_1','prompt':o['frame'],'aspect_ratio':'9:16','resolution':'2k','medias':[{'value':o['base'],'role':'image_references'},{'value':'d1c7b637-a322-4ef6-9c87-3d51c3bdfc56','role':'image_references'}]}} for i,o in enumerate(out)],ensure_ascii=False))

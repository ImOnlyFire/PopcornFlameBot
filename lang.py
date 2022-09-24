popcorn_types = ["Burro", "Caramellato", "Cioccolato", "Classico", "Extra Salato", "Mela Verde", "Miele"]
popcorn_image_link = 'https://i.imgur.com/2E5Tf9F.png'

popcorn_preparation = f"""
🍿 <b>Popcorn stand!</b>
Durante le sessioni di flame, i popcorn li offriamo <b>gratuitamente</b>.

<b>Gusti disponibili</b> ⟩
<i>{', '.join(popcorn_types)}</i>

Digita /cancel se hai perso la fame

°°°·.°·..·°¯°·._.·   🎀  🍿  🎀   ·._.·°¯°·..·°.·°°°
"""

popcorn_ready = f"""
<a href=\"{popcorn_image_link}\">&#8205</a>🍿 <b>I tuoi popcorn sono pronti!</b> 🍿
 ➜ 🥂 Gusto › {type}
 ➜ 💶 Costo › 0€

Grazie per aver scelto il nostro stand! <b>Buona visione</b>

<i>(Se ti piacciono i nostri popcorn, per favore lascia un feedback!)</i>
"""

no_flame_currently_active = """
Per poter ordinare i popcorn, deve esserci un flame attivo nel gruppo.
Chiedi ad un admin di digitare /flame se c'e' un flame in corso.
"""

flame_automatically_disabled = """
💧 Il gruppo è stato automaticamente rimosso dalla lista dei flame abilitati. 
Se c'è ancora un flame in corso, chiedi ad un admin di digitare /flame
"""

flame_mode_enabled = """
🔥 <b>Modalità flame abilitata</b>

Da questo momento in poi, i popcorn li offriamo <b>gratuitamente</b>!
Digita /popcorn per ordinare i popcorn

<i>La modalità flame resterà attivata per 25 minuti. </i>
<i>Se vuoi disattivarla, chiedi ad un admin di digitare /flame</i> 
"""

bot_joined = """
🍿 <b>Ciao</b>, grazie per avermi aggiunto al gruppo!
<i>C'è un flame nel gruppo? Mangia i popcorn e goditi lo spettacolo!</i>

Gli admin potranno utilizzare /flame in caso di un flame, e in questo periodo 
i popcorn li offriremo <b>gratuitamente</b> a tutti gli utenti del gruppo. (/popcorn)
"""

flame_mode_disabled = '<b>💧 Modalità flame disattivata</b>'

input_field_select_flavour = 'Scegli il gusto'
preparing_popcorn = 'Stiamo preparando i tuoi popcorn...'
private_chat_not_supported = 'Non puoi usare questo comando in privato.'
order_canceled = 'Ordine annullato.'
feedback_thanks = 'Grazie per il feedback!'
only_admins_command = 'Solo gli admin possono usare questo comando.'

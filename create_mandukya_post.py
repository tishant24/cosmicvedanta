import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cosmicvedanta.settings'
django.setup()

from blog.models import Post, Category
from accounts.models import CustomUser

cat, _ = Category.objects.get_or_create(name='Vedanta', defaults={'slug': 'vedanta'})
author = CustomUser.objects.first()

body = '''
<div class="mandukya-post">

<p class="post-intro">The Mandukya Upanishad &mdash; the shortest of all principal Upanishads, yet the most profound. In just 12 verses, it maps the entire architecture of consciousness, from the waking world you see right now to the infinite silence that holds it all together.</p>

<div class="vedanta-highlight">
<p><strong>The Mandukya Upanishad teaches that:</strong></p>
<p>&Amacr;tman (Self) = Brahman (Ultimate Reality)</p>
<p>The entire universe and consciousness are symbolized by <span class="om-symbol">&oplus;</span> (Om)</p>
</div>

<!-- MANTRA 1 -->
<h2>Mantra 1 &mdash; The Whole Universe is OM</h2>

<div class="sanskrit-block">
<p class="sanskrit-text">&oplus; इत्येतदक्षरमिदं सर्वम् । तस्योपव्याख्यानं भूतं भवद्भविष्यदिति सर्वमोङ्कार एव ।</p>
</div>

<blockquote>
Om is all this. Everything that existed in the past, exists now, and will exist in the future &mdash; everything is Om. Even that which is beyond time is also Om.
</blockquote>

<!-- MANTRA 2 -->
<h2>Mantra 2 &mdash; The Identity of Self and Brahman</h2>

<div class="sanskrit-block">
<p class="sanskrit-text">सर्वं ह्येतद्ब्रह्म । अयमात्मा ब्रह्म । सोऽयमात्मा चतुष्पात् ।</p>
</div>

<blockquote>
All this is indeed Brahman. This Self (&Amacr;tman) is Brahman. This same Self has four states (quarters).
</blockquote>

<!-- FOUR STATES -->
<h2>The Four States of Consciousness</h2>

<p>This is where the Mandukya becomes a mirror. It doesn't describe something distant &mdash; it describes <em>you</em>, right now, and every moment of your existence.</p>

<!-- STATE 1 -->
<div class="consciousness-state state-waking">
<h3>1. जाग्रत अवस्था &mdash; The Waking State (Vai&sacute;v&amacr;nara)</h3>

<div class="sanskrit-block">
<p class="sanskrit-text">जागरितस्थानो बहिष्प्रज्ञः सप्ताङ्ग एकोनविंशतिमुखः स्थूलभुग्वैश्वानरः प्रथमः पादः ।</p>
</div>

<blockquote>
The first state is the waking state, where consciousness is outward-facing. It experiences the gross world through the senses. This is called Vai&sacute;v&amacr;nara.
</blockquote>

<p><strong>This is you right now.</strong> Reading this screen. Aware of the room around you. Your consciousness points outward &mdash; toward objects, people, notifications, the hum of the world.</p>

<p>You work in your office. You scroll through feeds. You talk to people. And you believe: <em>"This is real life."</em></p>
</div>

<!-- STATE 2 -->
<div class="consciousness-state state-dream">
<h3>2. स्वप्न अवस्था &mdash; The Dream State (Taijasa)</h3>

<div class="sanskrit-block">
<p class="sanskrit-text">स्वप्नस्थानोऽन्तःप्रज्ञः सप्ताङ्ग एकोनविंशतिमुखः प्रविविक्तभुक्तैजसों द्वितीयः पादः ।</p>
</div>

<blockquote>
The second state is the dream state, where consciousness turns inward. It experiences subtle objects created by the mind. This is called Taijasa.
</blockquote>

<p>In dreams, you see people, places, emotions. Everything feels completely real. You laugh, you cry, you run, you fall &mdash; and you never question it.</p>

<p><strong>The Modern Parallel:</strong> A dream is Virtual Reality created entirely by the mind. No external world, yet fully experienced. If the mind can generate an entire universe while you sleep, how certain are you about the one it shows you while awake?</p>
</div>

<!-- STATE 3 -->
<div class="consciousness-state state-sleep">
<h3>3. सुषुप्ति अवस्था &mdash; Deep Sleep (Praj&ntilde;a)</h3>

<div class="sanskrit-block">
<p class="sanskrit-text">यत्र सुप्तो न कञ्चन कामं कामयते न कञ्चन स्वप्नं पश्यति तत्सुषुप्तम् ।</p>
<p class="sanskrit-text">सुषुप्तस्थान एकीभूतः प्रज्ञानघन एवानन्दमयो ह्यानन्दभुक् चेतोमुखः प्राज्ञस्तृतीयः पादः ।</p>
</div>

<blockquote>
In deep sleep, one neither desires anything nor sees any dream. Consciousness becomes unified, full of awareness, and blissful. This is called Praj&ntilde;a.
</blockquote>

<p>No stress. No identity. No name, no job title, no problems. Pure rest. And yet &mdash; you wake up and say <em>"I slept well."</em> Who was there to know?</p>

<p><strong>The Insight:</strong> Happiness in deep sleep comes from the <em>absence of mind</em>, not the presence of objects. You chase things in waking life for happiness, but the deepest peace comes when everything &mdash; including "you" &mdash; disappears.</p>
</div>

<!-- STATE 4 -->
<div class="consciousness-state state-turiya">
<h3>4. तुरीय &mdash; The Fourth: The Absolute State</h3>

<div class="sanskrit-block">
<p class="sanskrit-text">नान्तःप्रज्ञं न बहिःप्रज्ञं न उभयतःप्रज्ञं न प्रज्ञानघनम् । न प्रज्ञं नाप्रज्ञम् ।</p>
<p class="sanskrit-text">अदृष्टम् अव्यवहार्यम् अग्राह्यम् अलक्षणम् ।</p>
<p class="sanskrit-text">अचिन्त्यम् अव्यपदेश्यम् एकात्मप्रत्ययसारम् ।</p>
<p class="sanskrit-text">प्रपञ्चोपशमं शान्तं शिवम् अद्वैतम् चतुर्थं मन्यन्ते स आत्मा स विज्ञेयः ।</p>
</div>

<blockquote>
The fourth state is neither inward nor outward consciousness, nor both, nor a mass of cognition. It is unseen, beyond empirical dealings, incomprehensible, and indescribable. It is the cessation of all phenomena, peaceful, auspicious, and non-dual. <strong>This is the Self and must be realized.</strong>
</blockquote>

<p>Tur&imacr;ya is not a "state" like the others. It is the <em>screen</em> on which waking, dream, and deep sleep are projected. It is the unchanging awareness that witnesses all three states come and go.</p>

<p>It cannot be seen, because it is the seer. It cannot be thought, because it is the thinker. It cannot be described, because it is prior to all language.</p>
</div>

<!-- THE GAME-CHANGER -->
<h2>The Biggest Discovery</h2>

<div class="vedanta-highlight">
<p>You are present in Waking. You are present in Dream. You are present in Deep Sleep.</p>
<p>These states keep changing. <strong>You &mdash; the observer &mdash; do not.</strong></p>
</div>

<div class="sanskrit-block">
<p class="sanskrit-text">स आत्मा स विज्ञेयः</p>
<p><em>That is the Self to be realized.</em></p>
</div>

<p>Thoughts change. Emotions change. Your identity changes. Your body changes. But the silent <em>"I am aware"</em> &mdash; that has never changed, not even for a single moment since you were born.</p>

<!-- OM AND THE FOUR STATES -->
<h2>OM and the Four States</h2>

<div class="sanskrit-block">
<p class="sanskrit-text">सोऽयमात्मा अध्यक्षरं ओंकारः । अधिमात्रं पादा मात्रा मात्राश्च पादा अकार उकार मकार इति ।</p>
</div>

<blockquote>
This Self is represented by Om. Om has parts (A, U, M), and these correspond to the four states.
</blockquote>

<div class="om-breakdown">
<div class="om-part">
<h4>A (अ) &mdash; Waking</h4>
<div class="sanskrit-block">
<p class="sanskrit-text">जागरितस्थानो वैश्वानरोऽकारः प्रथमामात्रा ।</p>
</div>
<p>The sound "A" &mdash; the opening of the mouth, the beginning of all sound &mdash; represents the waking state.</p>
</div>

<div class="om-part">
<h4>U (उ) &mdash; Dream</h4>
<div class="sanskrit-block">
<p class="sanskrit-text">स्वप्नस्थानस्तैजस उकारो द्वितीयामात्रा ।</p>
</div>
<p>The sound "U" &mdash; the middle, the transition &mdash; represents the dream state where consciousness turns inward.</p>
</div>

<div class="om-part">
<h4>M (म) &mdash; Deep Sleep</h4>
<div class="sanskrit-block">
<p class="sanskrit-text">सुषुप्तस्थानः प्राज्ञो मकारस्तृतीयामात्रा ।</p>
</div>
<p>The sound "M" &mdash; the closing of the lips, the dissolution &mdash; represents deep sleep where everything merges.</p>
</div>

<div class="om-part om-silence">
<h4>Silence after OM &mdash; Tur&imacr;ya</h4>
<div class="sanskrit-block">
<p class="sanskrit-text">अमात्रश्चतुर्थोऽव्यवहार्यः प्रपञ्चोपशमः शिवोऽद्वैत एवम् ओंकार आत्मैव ।</p>
</div>
<p>The silence that follows &mdash; that pregnant emptiness after the "M" fades &mdash; <em>that</em> is Tur&imacr;ya. Beyond all transactions, peaceful, non-dual. <strong>It is the Self.</strong></p>
</div>
</div>

<p><strong>Practical Benefit of Chanting OM:</strong> It calms the nervous system, brings awareness inward, and connects you to deeper consciousness. Each chant is a complete journey through all four states of being.</p>

<!-- TODAY'S PROBLEMS -->
<h2>Today's Problems &amp; Mandukya Solutions</h2>

<div class="modern-problem">
<h3>Problem: Stress &amp; Overthinking</h3>
<p><strong>Cause:</strong> Identification with thoughts.</p>

<div class="sanskrit-block">
<p class="sanskrit-text">न प्रज्ञं नाप्रज्ञम्</p>
<p><em>The Self is beyond thought and no-thought.</em></p>
</div>

<p><strong>Solution:</strong> Observe thoughts instead of becoming them. You are not the storm &mdash; you are the sky in which the storm appears.</p>
</div>

<div class="modern-problem">
<h3>Problem: Identity Crisis</h3>
<p>Today people define themselves as their job title, social status, online image. Mandukya says: these belong to the waking state. They are temporary roles.</p>

<div class="sanskrit-block">
<p class="sanskrit-text">प्रपञ्चोपशमं</p>
<p><em>The cessation of all worldly appearances.</em></p>
</div>

<p><strong>Real identity:</strong> Not the roles, but the awareness behind all roles.</p>
</div>

<div class="modern-problem">
<h3>Problem: Fear of Loss &amp; Death</h3>
<p><strong>Fear comes from:</strong> "I am the body."</p>
<p>But your body exists only in the waking state. You exist in dreams without this body. You exist in deep sleep without any body at all. Therefore &mdash; <strong>you are not limited to the body.</strong></p>
</div>

<!-- MEDITATION -->
<h2>Meditation &amp; Mindfulness &mdash; The Mandukya Method</h2>

<p>The Mandukya is the highest form of meditation manual. Here is its practice distilled:</p>

<div class="meditation-steps">
<div class="med-step">
<h4>Step 1: Observe</h4>
<p>Notice your thoughts, emotions, and reactions without engaging. Just watch.</p>
</div>

<div class="med-step">
<h4>Step 2: Disidentify</h4>
<p>Instead of saying <em>"I am stressed"</em>, recognize: <em>"Stress is appearing in me."</em></p>
</div>

<div class="med-step">
<h4>Step 3: Recognize Awareness</h4>
<p>Ask: <strong>Who is aware of this thought?</strong></p>

<div class="sanskrit-block">
<p class="sanskrit-text">एकात्मप्रत्ययसारम्</p>
<p><em>The essence is the awareness of one Self.</em></p>
</div>
</div>
</div>

<!-- ULTIMATE REALIZATION -->
<h2>The Ultimate Realization</h2>

<div class="sanskrit-block">
<p class="sanskrit-text">शान्तं शिवम् अद्वैतम्</p>
<p><em>Peaceful. Auspicious. Non-dual.</em></p>
</div>

<p>When this is realized: no separation between self and world. No fear. No inner conflict. You stop <em>chasing</em> happiness. You realize <strong>you are happiness itself.</strong></p>

<div class="final-essence">
<div class="sanskrit-block">
<p class="sanskrit-text" style="font-size: 1.6em;">अयमात्मा ब्रह्म</p>
<p style="font-size: 1.2em;"><em>This Self is Brahman.</em></p>
</div>

<p class="closing-truth">You are not a person experiencing the universe.<br>
<strong>You are the awareness in which the universe appears.</strong></p>
</div>

</div>
'''

post, created = Post.objects.get_or_create(
    slug='mandukya-upanishad-essence-four-states-consciousness-om',
    defaults={
        'title': 'Mandukya Upanishad: The 12 Verses That Map the Entire Architecture of Consciousness',
        'author': author,
        'category': cat,
        'status': 'published',
        'is_featured': True,
        'excerpt': 'In just 12 verses, the Mandukya Upanishad reveals that you are not a person experiencing the universe — you are the awareness in which the universe appears. Explore the four states of consciousness and the sacred syllable OM.',
        'vedanta_quote': 'अयमात्मा ब्रह्म — This Self is Brahman. You are not a person experiencing the universe. You are the awareness in which the universe appears.',
        'vedanta_source': 'Mandukya Upanishad',
        'meta_title': 'Mandukya Upanishad Explained: Four States of Consciousness & OM | CosmicVedanta',
        'meta_description': 'Deep dive into the Mandukya Upanishad — the shortest yet most profound Upanishad. Explore Waking, Dream, Deep Sleep, Turiya, and the sacred syllable OM with Sanskrit verses and modern relevance.',
        'body': body,
    }
)

if created:
    print('Mandukya Upanishad post created successfully!')
else:
    print('Post already exists.')
